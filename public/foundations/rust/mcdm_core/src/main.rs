// MCDM Studio — Modelos Multicritério de Decisão
// Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
// E-mail: profbruanbima@gmail.com
//
//! CLI do motor MCDM em Rust.
//!
//! Lê um problema de decisão em texto simples e roda todos os métodos, imprimindo
//! o ranking de cada escola e o consenso de Borda. Sem dependências: um binário
//! estático que roda onde não há Python.
//!
//! Uso:
//!     mcdm <arquivo.mcdm>            # relatório em texto
//!     mcdm <arquivo.mcdm> --json     # saída JSON (para o pipeline Python conferir)
//!     mcdm --exemplo                 # imprime um arquivo de exemplo comentado
//!
//! Formato do arquivo (ver `--exemplo`):
//!     criterios: preco:cost autonomia:benefit recarga:cost
//!     alternativas: EV1 EV2 EV3
//!     matriz:
//!     480 520 22
//!     350 480 28
//!     240 330 35
//!     pesos: 0.5 0.3 0.2        # opcional — uniformes se ausente
//!     dematel:                  # opcional — se presente, os pesos saem daqui
//!     0 3 2
//!     2 0 3
//!     1 2 0

use mcdm_core::*;
use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::process;

const EXEMPLO: &str = r#"# Exemplo: aquisição de veículo elétrico para frota.
# Linhas iniciadas por '#' são comentários.
#
# Cada critério é declarado como  nome:direcao  onde direcao é 'cost' ou 'benefit'.
criterios: preco:cost autonomia:benefit recarga:cost consumo:cost revenda:benefit
alternativas: SUV_premium Seda_executivo Hatch_urbano SUV_chines Hibrido_plugin

# Linhas = alternativas, colunas = critérios, na ordem declarada acima.
matriz:
480 520 22 18.5 61
350 480 28 16.2 58
240 330 35 14.0 52
210 400 30 15.8 44
290 680 45 12.5 66

# Matriz de influência do DEMATEL (0=nenhuma .. 4=muito alta).
# Se presente, os PESOS são derivados dela por influência sistêmica,
# e a linha 'pesos:' passa a ser ignorada.
dematel:
0 3 2 1 3
2 0 3 3 3
1 2 0 1 2
2 4 2 0 2
1 0 0 0 0
"#;

struct Problema {
    criterios: Vec<String>,
    direcoes: Vec<Direcao>,
    alternativas: Vec<String>,
    matriz: Matriz,
    pesos: Option<Vec<f64>>,
    dematel: Option<Matriz>,
}

fn analisar(texto: &str) -> Result<Problema, String> {
    let mut criterios = Vec::new();
    let mut direcoes = Vec::new();
    let mut alternativas = Vec::new();
    let mut linhas_matriz: Vec<Vec<f64>> = Vec::new();
    let mut linhas_dematel: Vec<Vec<f64>> = Vec::new();
    let mut pesos = None;
    let mut secao = "";

    for (n, bruta) in texto.lines().enumerate() {
        let linha = bruta.split('#').next().unwrap_or("").trim();
        if linha.is_empty() {
            continue;
        }
        let num = n + 1;

        if let Some(resto) = linha.strip_prefix("criterios:") {
            secao = "";
            for item in resto.split_whitespace() {
                let (nome, dir) = item
                    .split_once(':')
                    .ok_or_else(|| format!("linha {num}: critério {item:?} sem ':direcao'"))?;
                criterios.push(nome.to_string());
                direcoes.push(Direcao::de_str(dir).map_err(|e| format!("linha {num}: {e}"))?);
            }
        } else if let Some(resto) = linha.strip_prefix("alternativas:") {
            secao = "";
            alternativas = resto.split_whitespace().map(String::from).collect();
        } else if let Some(resto) = linha.strip_prefix("pesos:") {
            secao = "";
            let v: Result<Vec<f64>, _> = resto.split_whitespace().map(str::parse::<f64>).collect();
            pesos = Some(v.map_err(|e| format!("linha {num}: peso inválido ({e})"))?);
        } else if linha.starts_with("matriz:") {
            secao = "matriz";
        } else if linha.starts_with("dematel:") {
            secao = "dematel";
        } else {
            let v: Result<Vec<f64>, _> = linha.split_whitespace().map(str::parse::<f64>).collect();
            let v = v.map_err(|e| format!("linha {num}: número inválido ({e})"))?;
            match secao {
                "matriz" => linhas_matriz.push(v),
                "dematel" => linhas_dematel.push(v),
                _ => return Err(format!("linha {num}: dado fora de seção — {linha:?}")),
            }
        }
    }

    if criterios.is_empty() {
        return Err("nenhum critério declarado (use 'criterios: nome:cost ...')".into());
    }
    if alternativas.is_empty() {
        return Err("nenhuma alternativa declarada".into());
    }
    if linhas_matriz.len() != alternativas.len() {
        return Err(format!(
            "matriz tem {} linhas para {} alternativas",
            linhas_matriz.len(),
            alternativas.len()
        ));
    }
    if let Some(l) = linhas_matriz.iter().position(|l| l.len() != criterios.len()) {
        return Err(format!(
            "linha {} da matriz tem {} valores para {} critérios",
            l + 1,
            linhas_matriz[l].len(),
            criterios.len()
        ));
    }

    let dados: Vec<f64> = linhas_matriz.into_iter().flatten().collect();
    let matriz = Matriz::de_vec(alternativas.len(), criterios.len(), dados)?;

    let dematel = if linhas_dematel.is_empty() {
        None
    } else {
        if linhas_dematel.len() != criterios.len() {
            return Err(format!(
                "DEMATEL tem {} linhas para {} critérios",
                linhas_dematel.len(),
                criterios.len()
            ));
        }
        let d: Vec<f64> = linhas_dematel.into_iter().flatten().collect();
        Some(Matriz::de_vec(criterios.len(), criterios.len(), d)?)
    };

    Ok(Problema { criterios, direcoes, alternativas, matriz, pesos, dematel })
}

fn escapar_json(s: &str) -> String {
    s.replace('\\', "\\\\").replace('"', "\\\"")
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 || args[1] == "-h" || args[1] == "--help" {
        eprintln!("MCDM Studio — motor de decisão multicritério (Rust)");
        eprintln!("Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS\n");
        eprintln!("Uso:  mcdm <arquivo.mcdm> [--json]");
        eprintln!("      mcdm --exemplo    imprime um arquivo de exemplo comentado");
        process::exit(if args.len() < 2 { 1 } else { 0 });
    }
    if args[1] == "--exemplo" {
        print!("{EXEMPLO}");
        return;
    }

    let json = args.iter().any(|a| a == "--json");
    let texto = match fs::read_to_string(&args[1]) {
        Ok(t) => t,
        Err(e) => {
            eprintln!("❌ não foi possível ler {:?}: {e}", args[1]);
            process::exit(1);
        }
    };
    let p = match analisar(&texto) {
        Ok(p) => p,
        Err(e) => {
            eprintln!("❌ erro no arquivo de problema: {e}");
            process::exit(1);
        }
    };

    // --- Pesos: DEMATEL tem precedência; depois 'pesos:'; depois uniformes ----
    let (pesos, origem_pesos, saida_dematel) = match &p.dematel {
        Some(z) => match dematel(z) {
            Ok(s) => (s.pesos.clone(), "DEMATEL (influência sistêmica)", Some(s)),
            Err(e) => {
                eprintln!("❌ DEMATEL: {e}");
                process::exit(1);
            }
        },
        None => match &p.pesos {
            Some(w) => (w.clone(), "declarados no arquivo", None),
            None => (
                vec![1.0 / p.criterios.len() as f64; p.criterios.len()],
                "uniformes (nenhum peso informado)",
                None,
            ),
        },
    };

    // --- Roda todos os métodos ----------------------------------------------
    let mut scores: BTreeMap<&str, Vec<f64>> = BTreeMap::new();
    macro_rules! rodar {
        ($nome:expr, $expr:expr) => {
            match $expr {
                Ok(v) => {
                    scores.insert($nome, v);
                }
                Err(e) => {
                    eprintln!("❌ {}: {e}", $nome);
                    process::exit(1);
                }
            }
        };
    }
    rodar!("AHP-TOPSIS 2n", topsis_2n(&p.matriz, &pesos, &p.direcoes));
    rodar!("ELECTRE I", electre_i(&p.matriz, &pesos, &p.direcoes, 0.65, 0.35).map(|s| s.score));
    rodar!("ELECTRE II", electre_ii(&p.matriz, &pesos, &p.direcoes, 0.75, 0.60, 0.25, 0.40).map(|s| s.score));
    rodar!("MAUT", maut(&p.matriz, &pesos, &p.direcoes, 2.0));
    rodar!("MCDA-C", mcda_c(&p.matriz, &pesos, &p.direcoes, 0.25, 0.75));
    rodar!("PROMETHEE II", promethee_ii(&p.matriz, &pesos, &p.direcoes, FuncaoPreferencia::Linear));
    rodar!("TODIM", todim(&p.matriz, &pesos, &p.direcoes, 1.0));
    rodar!("SAPEVO-M", sapevo_m_de_matriz(&p.matriz, &pesos, &p.direcoes));
    rodar!("TOPSIS Fuzzy", fuzzy_topsis(&p.matriz, &pesos, &p.direcoes, FUZZY_ALPHA));
    let saida_vikor = match vikor(&p.matriz, &pesos, &p.direcoes, 0.5) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("❌ VIKOR: {e}");
            process::exit(1);
        }
    };
    scores.insert("VIKOR", saida_vikor.score.clone());

    let posicoes: BTreeMap<&str, Vec<usize>> =
        scores.iter().map(|(k, v)| (*k, ranks(v))).collect();
    let pontos = borda(&posicoes.values().cloned().collect::<Vec<_>>(), p.alternativas.len());
    let consenso = ranks(&pontos);
    let vencedor = consenso.iter().position(|&r| r == 1).unwrap_or(0);

    // --- Saída ---------------------------------------------------------------
    if json {
        println!("{{");
        println!("  \"origem_pesos\": \"{}\",", escapar_json(origem_pesos));
        println!("  \"criterios\": [{}],", p.criterios.iter()
            .map(|c| format!("\"{}\"", escapar_json(c))).collect::<Vec<_>>().join(", "));
        println!("  \"pesos\": [{}],", pesos.iter()
            .map(|w| format!("{w:.10}")).collect::<Vec<_>>().join(", "));
        println!("  \"alternativas\": [{}],", p.alternativas.iter()
            .map(|a| format!("\"{}\"", escapar_json(a))).collect::<Vec<_>>().join(", "));
        println!("  \"metodos\": {{");
        let n = scores.len();
        for (i, (nome, sc)) in scores.iter().enumerate() {
            let virgula = if i + 1 < n { "," } else { "" };
            println!("    \"{}\": {{ \"score\": [{}], \"rank\": [{}] }}{virgula}",
                escapar_json(nome),
                sc.iter().map(|v| format!("{v:.10}")).collect::<Vec<_>>().join(", "),
                posicoes[nome.as_ref() as &str].iter()
                    .map(|r| r.to_string()).collect::<Vec<_>>().join(", "));
        }
        println!("  }},");
        println!("  \"consenso_borda\": [{}],",
            consenso.iter().map(|r| r.to_string()).collect::<Vec<_>>().join(", "));
        println!("  \"vencedor\": \"{}\",", escapar_json(&p.alternativas[vencedor]));
        println!("  \"vikor\": {{ \"c1\": {}, \"c2\": {} }}",
            saida_vikor.c1_vantagem_aceitavel, saida_vikor.c2_estabilidade_aceitavel);
        println!("}}");
        return;
    }

    let largura = 22 + scores.len() * 15 + 11;
    println!("\n{}", "═".repeat(largura));
    println!(" MCDM Studio · motor Rust — {} alternativas × {} critérios",
        p.alternativas.len(), p.criterios.len());
    println!(" pesos: {origem_pesos}");
    println!("{}", "═".repeat(largura));

    if let Some(s) = &saida_dematel {
        println!("\n▸ DEMATEL — estrutura causal (limiar α = {:.4})", s.limiar);
        println!("  {:<20} {:>9} {:>9}  {:<7} {:>8}", "CRITÉRIO", "R+C", "R−C", "PAPEL", "PESO");
        let mut ordem: Vec<usize> = (0..p.criterios.len()).collect();
        ordem.sort_by(|&a, &b| s.prominencia[b].partial_cmp(&s.prominencia[a]).unwrap());
        for i in ordem {
            println!("  {:<20} {:>9.3} {:>+9.3}  {:<7} {:>7.2}%",
                p.criterios[i], s.prominencia[i], s.relacao[i],
                if s.eh_causa(i) { "CAUSA" } else { "efeito" }, s.pesos[i] * 100.0);
        }
    }

    println!("\n▸ RANKING POR ESCOLA DE DECISÃO");
    print!("  {:<20}", "ALTERNATIVA");
    for nome in scores.keys() {
        print!("{nome:>15}");
    }
    println!("{:>11}", "CONSENSO");
    println!("  {}", "─".repeat(largura - 2));

    let mut ordem: Vec<usize> = (0..p.alternativas.len()).collect();
    ordem.sort_by_key(|&i| consenso[i]);
    for i in ordem {
        print!("  {:<20}", p.alternativas[i]);
        for nome in scores.keys() {
            print!("{:>14}º", posicoes[nome.as_ref() as &str][i]);
        }
        println!("{:>10}º", consenso[i]);
    }

    println!("\n▸ VIKOR — solução de compromisso");
    println!("  C1 (vantagem aceitável):    {}", if saida_vikor.c1_vantagem_aceitavel { "sim" } else { "NÃO" });
    println!("  C2 (estabilidade aceitável): {}", if saida_vikor.c2_estabilidade_aceitavel { "sim" } else { "NÃO" });
    print!("  conjunto de compromisso: ");
    println!("{}", saida_vikor.conjunto_compromisso.iter()
        .map(|&i| p.alternativas[i].as_str()).collect::<Vec<_>>().join(", "));

    println!("\n{}", "─".repeat(largura));
    println!(" 🏆 VENCEDOR (consenso de Borda entre {} métodos): {}",
        scores.len(), p.alternativas[vencedor]);
    println!("{}", "─".repeat(largura));
}
