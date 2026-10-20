// MCDM Studio — Modelos Multicritério de Decisão
// Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
// E-mail: profbruanbima@gmail.com
//
//! Motor de decisão multicritério em Rust.
//!
//! # Por que uma segunda implementação
//!
//! A implementação de referência do projeto é Python + NumPy/numba. Este crate
//! existe por três razões concretas, não por gosto:
//!
//! 1. **Verificação cruzada.** Dois motores independentes que concordam no
//!    ranking até 1e-9 são uma evidência forte de que a matemática está certa.
//!    Um erro de transcrição de fórmula raramente se repete idêntico em duas
//!    linguagens com autores de código diferentes. É a tripla-checagem levada ao
//!    nível do algoritmo (ver `_private/foundations/triplecheck.md`).
//! 2. **Distribuição sem runtime.** Um binário estático de poucos MB roda em
//!    servidor, contêiner ou máquina embarcada sem Python, sem NumPy, sem numba
//!    e sem ambiente virtual — o que importa quando o motor precisa acompanhar
//!    um sistema em campo.
//! 3. **Previsibilidade.** Sem GIL, sem coletor de lixo e sem JIT aquecendo na
//!    primeira chamada: o mesmo tempo de resposta na primeira e na milésima
//!    execução.
//!
//! # Convenção do motor
//!
//! Toda função de ranqueamento devolve um vetor de *scores* em que **maior é
//! sempre melhor**, mesmo para métodos cuja formulação original minimiza (VIKOR).
//! Isso permite compor qualquer subconjunto de métodos no consenso de Borda sem
//! casos especiais.
//!
//! # Procedência dos métodos
//!
//! DEMATEL — Gabus & Fontela (Battelle, 1972-73).
//! ELECTRE I — Roy (1968).  ELECTRE II — Roy & Bertier (1971).
//! PROMETHEE II — Brans & Vincke (1985).
//! MAUT — Keeney & Raiffa (1976).  MCDA-C — Ensslin et al. (2001).
//! AHP — Saaty (1980).  TOPSIS — Hwang & Yoon (1981).
//! VIKOR — Opricovic (1979); Opricovic & Tzeng (2002, 2004, 2007).
//! TODIM — Gomes & Lima (1992); Gomes (2004); Kahneman & Tversky (1979).
//! SAPEVO-M — Gomes et al. (1997); Teixeira, Santos & Gomes (SPOLM/CASNAV, 2019).
//! Borda (1781); Copeland (1951).
//!
//! Os métodos da escola brasileira seguem os trabalhos reunidos em
//! `_private/foundations/kb/Artigos e Teses/Novos/` — ver `metodos_br.py` para a
//! citação completa de cada autor.

/// Direção do critério: maior é melhor, ou menor é melhor.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Direcao {
    /// Benefício — maior é melhor (autonomia, potência, nota).
    Beneficio,
    /// Custo — menor é melhor (preço, peso, tempo de recarga).
    Custo,
}

impl Direcao {
    pub fn de_str(s: &str) -> Result<Self, String> {
        match s.trim().to_lowercase().as_str() {
            "benefit" | "beneficio" | "benefício" | "max" | "+" => Ok(Direcao::Beneficio),
            "cost" | "custo" | "min" | "-" => Ok(Direcao::Custo),
            outro => Err(format!("direção desconhecida: {outro:?} (use benefit|cost)")),
        }
    }
}

/// Matriz densa em ordem de linhas (row-major).
#[derive(Debug, Clone, PartialEq)]
pub struct Matriz {
    pub linhas: usize,
    pub colunas: usize,
    pub dados: Vec<f64>,
}

impl Matriz {
    pub fn nova(linhas: usize, colunas: usize) -> Self {
        Matriz { linhas, colunas, dados: vec![0.0; linhas * colunas] }
    }

    pub fn de_vec(linhas: usize, colunas: usize, dados: Vec<f64>) -> Result<Self, String> {
        if dados.len() != linhas * colunas {
            return Err(format!(
                "esperados {} valores para {linhas}×{colunas}, recebidos {}",
                linhas * colunas,
                dados.len()
            ));
        }
        Ok(Matriz { linhas, colunas, dados })
    }

    #[inline(always)]
    pub fn get(&self, i: usize, j: usize) -> f64 {
        self.dados[i * self.colunas + j]
    }

    #[inline(always)]
    pub fn set(&mut self, i: usize, j: usize, v: f64) {
        self.dados[i * self.colunas + j] = v;
    }

    pub fn coluna(&self, j: usize) -> Vec<f64> {
        (0..self.linhas).map(|i| self.get(i, j)).collect()
    }

    pub fn quadrada(&self) -> bool {
        self.linhas == self.colunas
    }
}

// ===========================================================================
// Utilidades numéricas
// ===========================================================================

/// Normaliza pesos para somar 1, validando positividade.
pub fn normalizar_pesos(w: &[f64], n: usize) -> Result<Vec<f64>, String> {
    if w.len() != n {
        return Err(format!("pesos: esperados {n}, recebidos {}", w.len()));
    }
    if w.iter().any(|&x| x < 0.0) {
        return Err("pesos negativos não fazem sentido em MCDM".into());
    }
    let soma: f64 = w.iter().sum();
    if soma <= 0.0 {
        return Err("soma dos pesos é zero".into());
    }
    Ok(w.iter().map(|x| x / soma).collect())
}

/// Normaliza a matriz para [0,1] embutindo a direção: na saída MAIOR é SEMPRE MELHOR.
///
/// Coluna constante vira 0,5 (indiferença) — zerá-la embutiria um viés, punindo
/// toda alternativa num critério em que ninguém se distingue.
pub fn orientar(x: &Matriz, direcoes: &[Direcao]) -> Result<Matriz, String> {
    if direcoes.len() != x.colunas {
        return Err(format!(
            "direções: esperadas {}, recebidas {}",
            x.colunas,
            direcoes.len()
        ));
    }
    let mut g = Matriz::nova(x.linhas, x.colunas);
    for j in 0..x.colunas {
        let col = x.coluna(j);
        let lo = col.iter().cloned().fold(f64::INFINITY, f64::min);
        let hi = col.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        for i in 0..x.linhas {
            let v = if hi <= lo {
                0.5
            } else if direcoes[j] == Direcao::Beneficio {
                (col[i] - lo) / (hi - lo)
            } else {
                (hi - col[i]) / (hi - lo)
            };
            g.set(i, j, v);
        }
    }
    Ok(g)
}

/// Posições a partir de scores: 1 = melhor (maior score). Estável em empates.
pub fn ranks(score: &[f64]) -> Vec<usize> {
    let mut idx: Vec<usize> = (0..score.len()).collect();
    // Ordena decrescente; empate resolvido pelo índice original (estabilidade).
    idx.sort_by(|&a, &b| {
        score[b]
            .partial_cmp(&score[a])
            .unwrap_or(std::cmp::Ordering::Equal)
            .then(a.cmp(&b))
    });
    let mut rk = vec![0usize; score.len()];
    for (pos, &i) in idx.iter().enumerate() {
        rk[i] = pos + 1;
    }
    rk
}

/// Quantil por interpolação linear — equivalente ao `numpy.quantile` padrão.
///
/// A equivalência importa: PROMETHEE e MCDA-C ancoram limiares em quantis, e uma
/// definição diferente de quantil faria os dois motores divergirem por um motivo
/// que não é matemático, e sim de convenção.
pub fn quantil(v: &[f64], q: f64) -> f64 {
    if v.is_empty() {
        return 0.0;
    }
    let mut s = v.to_vec();
    s.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    if s.len() == 1 {
        return s[0];
    }
    let pos = q.clamp(0.0, 1.0) * (s.len() - 1) as f64;
    let baixo = pos.floor() as usize;
    let alto = pos.ceil() as usize;
    if baixo == alto {
        s[baixo]
    } else {
        s[baixo] + (pos - baixo as f64) * (s[alto] - s[baixo])
    }
}

/// Resolve A·X = B por eliminação gaussiana com pivotamento parcial.
pub fn resolver(a: &Matriz, b: &Matriz) -> Result<Matriz, String> {
    if !a.quadrada() || a.linhas != b.linhas {
        return Err("resolver: dimensões incompatíveis".into());
    }
    let n = a.linhas;
    let m = b.colunas;
    let mut aa = a.dados.clone();
    let mut bb = b.dados.clone();

    for col in 0..n {
        // Pivotamento parcial: reduz o erro de arredondamento acumulado.
        let mut piv = col;
        for l in (col + 1)..n {
            if aa[l * n + col].abs() > aa[piv * n + col].abs() {
                piv = l;
            }
        }
        if aa[piv * n + col].abs() < 1e-14 {
            return Err("matriz singular ou mal condicionada".into());
        }
        if piv != col {
            for j in 0..n {
                aa.swap(col * n + j, piv * n + j);
            }
            for j in 0..m {
                bb.swap(col * m + j, piv * m + j);
            }
        }
        let d = aa[col * n + col];
        for l in (col + 1)..n {
            let fator = aa[l * n + col] / d;
            if fator == 0.0 {
                continue;
            }
            for j in col..n {
                aa[l * n + j] -= fator * aa[col * n + j];
            }
            for j in 0..m {
                bb[l * m + j] -= fator * bb[col * m + j];
            }
        }
    }
    // Retrossubstituição.
    for col in (0..n).rev() {
        let d = aa[col * n + col];
        for j in 0..m {
            let mut soma = bb[col * m + j];
            for l in (col + 1)..n {
                soma -= aa[col * n + l] * bb[l * m + j];
            }
            bb[col * m + j] = soma / d;
        }
    }
    Matriz::de_vec(n, m, bb)
}

// ===========================================================================
// DEMATEL — Gabus & Fontela (Battelle).
// ===========================================================================

#[derive(Debug, Clone)]
pub struct SaidaDematel {
    pub r: Vec<f64>,
    pub c: Vec<f64>,
    pub prominencia: Vec<f64>,
    pub relacao: Vec<f64>,
    pub pesos: Vec<f64>,
    pub t: Matriz,
    pub limiar: f64,
}

impl SaidaDematel {
    /// `true` se o critério é CAUSA (alavanca), `false` se é EFEITO (termômetro).
    pub fn eh_causa(&self, i: usize) -> bool {
        self.relacao[i] > 0.0
    }
}

/// Matriz de relação direta Z -> estrutura causal e pesos por influência.
///
/// T = X(I − X)⁻¹ soma a série de Neumann ΣXᵏ: captura influência direta E
/// indireta, de qualquer comprimento de caminho. Resolvemos (I−X)ᵀ Yᵀ = Xᵀ em vez
/// de formar a inversa — mais estável e mais barato.
pub fn dematel(z: &Matriz) -> Result<SaidaDematel, String> {
    if !z.quadrada() {
        return Err(format!("DEMATEL exige matriz quadrada, recebida {}×{}", z.linhas, z.colunas));
    }
    let n = z.linhas;
    let max_linha = (0..n)
        .map(|i| (0..n).map(|j| z.get(i, j)).sum::<f64>())
        .fold(f64::NEG_INFINITY, f64::max);
    let max_coluna = (0..n)
        .map(|j| (0..n).map(|i| z.get(i, j)).sum::<f64>())
        .fold(f64::NEG_INFINITY, f64::max);
    let s = max_linha.max(max_coluna);
    if s <= 0.0 {
        return Err("matriz DEMATEL é toda zero: nenhuma influência declarada".into());
    }

    // Monta (I − X)ᵀ e Xᵀ, resolve, e transpõe de volta.
    let mut a = Matriz::nova(n, n);
    let mut xt = Matriz::nova(n, n);
    for i in 0..n {
        for j in 0..n {
            let x = z.get(i, j) / s;
            a.set(j, i, if i == j { 1.0 - x } else { -x });
            xt.set(j, i, x);
        }
    }
    let yt = resolver(&a, &xt)?;
    let mut t = Matriz::nova(n, n);
    for i in 0..n {
        for j in 0..n {
            t.set(i, j, yt.get(j, i));
        }
    }

    let r: Vec<f64> = (0..n).map(|i| (0..n).map(|j| t.get(i, j)).sum()).collect();
    let c: Vec<f64> = (0..n).map(|j| (0..n).map(|i| t.get(i, j)).sum()).collect();
    let prominencia: Vec<f64> = r.iter().zip(&c).map(|(a, b)| a + b).collect();
    let relacao: Vec<f64> = r.iter().zip(&c).map(|(a, b)| a - b).collect();

    let brutos: Vec<f64> = prominencia
        .iter()
        .zip(&relacao)
        .map(|(p, rl)| (p * p + rl * rl).sqrt())
        .collect();
    let soma: f64 = brutos.iter().sum();
    let pesos = brutos.iter().map(|x| x / soma).collect();
    let limiar = t.dados.iter().sum::<f64>() / (n * n) as f64;

    Ok(SaidaDematel { r, c, prominencia, relacao, pesos, t, limiar })
}

// ===========================================================================
// AHP — Saaty (1980).
// ===========================================================================

/// Índice Aleatório de Saaty, tabelado até n = 15 (Saaty 1980; Alonso & Lamata 2006).
pub const RI: [f64; 16] = [
    0.00, 0.00, 0.00, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51, 1.48, 1.56,
    1.57, 1.59,
];

#[derive(Debug, Clone)]
pub struct SaidaAhp {
    pub pesos: Vec<f64>,
    pub cr: f64,
    pub lambda_max: f64,
}

impl SaidaAhp {
    /// CR < 0,10 => julgamentos par a par aceitáveis (critério de Saaty).
    pub fn consistente(&self) -> bool {
        self.cr < 0.10
    }
}

/// Pesos AHP pelo autovetor principal (método das potências) + razão de consistência.
///
/// O método das potências converge para o autovetor do autovalor de MAIOR MÓDULO
/// (Perron-Frobenius) — que é o correto para matrizes recíprocas positivas, e não
/// necessariamente o de maior parte real.
pub fn pesos_ahp(a: &Matriz) -> Result<SaidaAhp, String> {
    if !a.quadrada() {
        return Err("AHP exige matriz quadrada".into());
    }
    if a.dados.iter().any(|&x| x <= 0.0) {
        return Err("matriz de Saaty deve ser positiva (escala 1/9..9)".into());
    }
    let n = a.linhas;
    let mut v = vec![1.0 / n as f64; n];

    for _ in 0..1000 {
        let mut nv = vec![0.0; n];
        for i in 0..n {
            for j in 0..n {
                nv[i] += a.get(i, j) * v[j];
            }
        }
        let soma: f64 = nv.iter().sum();
        if soma.abs() < 1e-300 {
            return Err("AHP: iteração degenerou".into());
        }
        for x in nv.iter_mut() {
            *x /= soma;
        }
        let delta: f64 = nv.iter().zip(&v).map(|(a, b)| (a - b).abs()).sum();
        v = nv;
        if delta < 1e-14 {
            break;
        }
    }
    // λmax pelo quociente de Rayleigh na forma (Av)ᵢ / vᵢ, promediado.
    let mut soma_l = 0.0;
    for i in 0..n {
        let av: f64 = (0..n).map(|j| a.get(i, j) * v[j]).sum();
        soma_l += av / v[i];
    }
    let lambda_max = soma_l / n as f64;

    let cr = if n <= 2 {
        0.0
    } else {
        let ri = if n < RI.len() { RI[n] } else { 0.00149 * n as f64 + 1.3454 };
        ((lambda_max - n as f64) / (n as f64 - 1.0)) / ri
    };
    Ok(SaidaAhp { pesos: v, cr, lambda_max })
}

// ===========================================================================
// TOPSIS — Hwang & Yoon (1981); variante 2N (dupla normalização).
// ===========================================================================

/// Coeficiente de proximidade Ci ∈ [0,1] com normalização vetorial (Euclidiana).
pub fn topsis_vetorial(x: &Matriz, w: &[f64], direcoes: &[Direcao]) -> Result<Vec<f64>, String> {
    let w = normalizar_pesos(w, x.colunas)?;
    let mut v = Matriz::nova(x.linhas, x.colunas);
    for j in 0..x.colunas {
        let norma: f64 = (0..x.linhas).map(|i| x.get(i, j).powi(2)).sum::<f64>().sqrt();
        let norma = if norma == 0.0 { 1.0 } else { norma };
        for i in 0..x.linhas {
            v.set(i, j, x.get(i, j) / norma * w[j]);
        }
    }
    let mut ideal_pos = vec![0.0; x.colunas];
    let mut ideal_neg = vec![0.0; x.colunas];
    for j in 0..x.colunas {
        let col = v.coluna(j);
        let alto = col.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let baixo = col.iter().cloned().fold(f64::INFINITY, f64::min);
        if direcoes[j] == Direcao::Beneficio {
            ideal_pos[j] = alto;
            ideal_neg[j] = baixo;
        } else {
            ideal_pos[j] = baixo;
            ideal_neg[j] = alto;
        }
    }
    Ok(proximidade(&v, &ideal_pos, &ideal_neg))
}

/// Ci com normalização min-max (direção já embutida).
pub fn topsis_minmax(x: &Matriz, w: &[f64], direcoes: &[Direcao]) -> Result<Vec<f64>, String> {
    let w = normalizar_pesos(w, x.colunas)?;
    let g = orientar(x, direcoes)?;
    let mut v = Matriz::nova(g.linhas, g.colunas);
    for i in 0..g.linhas {
        for j in 0..g.colunas {
            v.set(i, j, g.get(i, j) * w[j]);
        }
    }
    let ideal_pos: Vec<f64> = (0..v.colunas)
        .map(|j| v.coluna(j).iter().cloned().fold(f64::NEG_INFINITY, f64::max))
        .collect();
    let ideal_neg: Vec<f64> = (0..v.colunas)
        .map(|j| v.coluna(j).iter().cloned().fold(f64::INFINITY, f64::min))
        .collect();
    Ok(proximidade(&v, &ideal_pos, &ideal_neg))
}

fn proximidade(v: &Matriz, ideal_pos: &[f64], ideal_neg: &[f64]) -> Vec<f64> {
    (0..v.linhas)
        .map(|i| {
            let d_pos: f64 = (0..v.colunas)
                .map(|j| (v.get(i, j) - ideal_pos[j]).powi(2))
                .sum::<f64>()
                .sqrt();
            let d_neg: f64 = (0..v.colunas)
                .map(|j| (v.get(i, j) - ideal_neg[j]).powi(2))
                .sum::<f64>()
                .sqrt();
            let soma = d_pos + d_neg;
            if soma == 0.0 { 0.0 } else { d_neg / soma }
        })
        .collect()
}

/// AHP-TOPSIS 2N: média das duas normalizações.
///
/// Rodar as duas e comparar transforma a sensibilidade do TOPSIS à normalização
/// em INFORMAÇÃO: se o ranking muda conforme a normalização, ele não deveria ir
/// ao comitê como se fosse um fato.
pub fn topsis_2n(x: &Matriz, w: &[f64], direcoes: &[Direcao]) -> Result<Vec<f64>, String> {
    let a = topsis_vetorial(x, w, direcoes)?;
    let b = topsis_minmax(x, w, direcoes)?;
    Ok(a.iter().zip(&b).map(|(p, q)| (p + q) / 2.0).collect())
}

// ===========================================================================
// ELECTRE I — Roy (1968).
// ===========================================================================

#[derive(Debug, Clone)]
pub struct SaidaElectre {
    pub score: Vec<f64>,
    pub nucleo: Vec<usize>,
    pub sobreclassifica: Vec<bool>,
    pub n: usize,
}

fn concordancia_discordancia(g: &Matriz, w: &[f64]) -> (Matriz, Matriz) {
    let m = g.linhas;
    let mut c = Matriz::nova(m, m);
    let mut d = Matriz::nova(m, m);
    for a in 0..m {
        for b in 0..m {
            if a == b {
                continue;
            }
            let mut conc = 0.0;
            let mut disc: f64 = 0.0;
            for j in 0..g.colunas {
                if g.get(a, j) >= g.get(b, j) {
                    conc += w[j];
                } else {
                    disc = disc.max(g.get(b, j) - g.get(a, j));
                }
            }
            c.set(a, b, conc);
            d.set(a, b, disc);
        }
    }
    (c, d)
}

/// ELECTRE I: grau de sobreclassificação líquido e núcleo (kernel) de Roy.
pub fn electre_i(
    x: &Matriz,
    w: &[f64],
    direcoes: &[Direcao],
    c_limiar: f64,
    d_limiar: f64,
) -> Result<SaidaElectre, String> {
    let w = normalizar_pesos(w, x.colunas)?;
    let g = orientar(x, direcoes)?;
    let m = g.linhas;
    let (c, d) = concordancia_discordancia(&g, &w);

    let mut s = vec![false; m * m];
    for a in 0..m {
        for b in 0..m {
            if a != b && c.get(a, b) >= c_limiar && d.get(a, b) <= d_limiar {
                s[a * m + b] = true;
            }
        }
    }
    let score: Vec<f64> = (0..m)
        .map(|a| {
            let domina = (0..m).filter(|&b| s[a * m + b]).count() as f64;
            let dominada = (0..m).filter(|&b| s[b * m + a]).count() as f64;
            domina - dominada
        })
        .collect();
    let nucleo: Vec<usize> = (0..m).filter(|&a| !(0..m).any(|b| s[b * m + a])).collect();
    Ok(SaidaElectre { score, nucleo, sobreclassifica: s, n: m })
}

// ===========================================================================
// ELECTRE II — Roy & Bertier (1971). Via Gomes Júnior (SPOLM 2008).
// ===========================================================================

#[derive(Debug, Clone)]
pub struct SaidaElectreIi {
    pub score: Vec<f64>,
    pub descendente: Vec<usize>,
    pub ascendente: Vec<usize>,
}

fn destilar(relacao: &[bool], m: usize, descendente: bool) -> Vec<usize> {
    let mut posicao = vec![0usize; m];
    let mut restantes: Vec<usize> = (0..m).collect();
    let mut nivel = 1;
    while !restantes.is_empty() {
        let livres: Vec<usize> = restantes
            .iter()
            .cloned()
            .filter(|&i| {
                if descendente {
                    // ninguém do grupo o sobreclassifica
                    !restantes.iter().any(|&k| k != i && relacao[k * m + i])
                } else {
                    // ele não sobreclassifica ninguém do grupo
                    !restantes.iter().any(|&k| k != i && relacao[i * m + k])
                }
            })
            .collect();
        // Ciclo de preferência: nenhum livre => corta o nível inteiro.
        let livres = if livres.is_empty() { restantes.clone() } else { livres };
        for &i in &livres {
            posicao[i] = nivel;
        }
        restantes.retain(|i| !livres.contains(i));
        nivel += 1;
    }
    posicao
}

/// ELECTRE II: pré-ordem COMPLETA por dupla destilação (descendente e ascendente).
pub fn electre_ii(
    x: &Matriz,
    w: &[f64],
    direcoes: &[Direcao],
    c_forte: f64,
    c_fraca: f64,
    d_forte: f64,
    d_fraca: f64,
) -> Result<SaidaElectreIi, String> {
    if c_fraca > c_forte || d_forte > d_fraca {
        return Err("ELECTRE II: exige c_fraca ≤ c_forte e d_forte ≤ d_fraca".into());
    }
    let w = normalizar_pesos(w, x.colunas)?;
    let g = orientar(x, direcoes)?;
    let m = g.linhas;
    let (c, d) = concordancia_discordancia(&g, &w);

    let mut forte = vec![false; m * m];
    let mut fraca = vec![false; m * m];
    for a in 0..m {
        for b in 0..m {
            if a == b {
                continue;
            }
            forte[a * m + b] = c.get(a, b) >= c_forte && d.get(a, b) <= d_forte;
            fraca[a * m + b] = c.get(a, b) >= c_fraca && d.get(a, b) <= d_fraca;
        }
    }
    let desc = destilar(&forte, m, true);
    let asc = destilar(&fraca, m, false);
    let max_asc = *asc.iter().max().unwrap_or(&1);
    let asc_inv: Vec<usize> = asc.iter().map(|&p| max_asc + 1 - p).collect();
    let score: Vec<f64> = (0..m)
        .map(|i| -((desc[i] + asc_inv[i]) as f64 / 2.0))
        .collect();
    Ok(SaidaElectreIi { score, descendente: desc, ascendente: asc_inv })
}

// ===========================================================================
// PROMETHEE II — Brans & Vincke (1985).
// ===========================================================================

/// As 6 funções de preferência generalizadas.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FuncaoPreferencia {
    Usual,
    UShape,
    VShape,
    Level,
    Linear,
    Gaussiana,
}

impl FuncaoPreferencia {
    pub fn de_str(s: &str) -> Result<Self, String> {
        match s.trim().to_lowercase().as_str() {
            "usual" => Ok(Self::Usual),
            "u-shape" | "ushape" => Ok(Self::UShape),
            "v-shape" | "vshape" => Ok(Self::VShape),
            "level" => Ok(Self::Level),
            "linear" => Ok(Self::Linear),
            "gaussian" | "gaussiana" => Ok(Self::Gaussiana),
            o => Err(format!("função de preferência desconhecida: {o:?}")),
        }
    }

    #[inline]
    pub fn avaliar(&self, d: f64, q: f64, p: f64, s: f64) -> f64 {
        if d <= 0.0 {
            return 0.0;
        }
        match self {
            Self::Usual => 1.0,
            Self::UShape => if d > q { 1.0 } else { 0.0 },
            Self::VShape => if d < p { d / p } else { 1.0 },
            Self::Level => {
                if d <= q { 0.0 } else if d <= p { 0.5 } else { 1.0 }
            }
            Self::Linear => {
                if d <= q { 0.0 } else if d >= p { 1.0 } else { (d - q) / (p - q) }
            }
            Self::Gaussiana => 1.0 - (-(d * d) / (2.0 * s * s)).exp(),
        }
    }
}

/// Fluxo líquido φ = φ⁺ − φ⁻ (pré-ordem completa).
///
/// Limiares q e p tirados dos quantis 10% e 90% dos desvios observados em cada
/// critério — prática usual quando não há limiares elicitados com o decisor.
pub fn promethee_ii(
    x: &Matriz,
    w: &[f64],
    direcoes: &[Direcao],
    funcao: FuncaoPreferencia,
) -> Result<Vec<f64>, String> {
    let w = normalizar_pesos(w, x.colunas)?;
    let g = orientar(x, direcoes)?;
    let m = g.linhas;
    let k = g.colunas;

    let mut qs = vec![0.0; k];
    let mut ps = vec![1.0; k];
    let mut ss = vec![0.5; k];
    for j in 0..k {
        let mut desvios = Vec::with_capacity(m * (m - 1).max(1));
        for a in 0..m {
            for b in 0..m {
                if a != b {
                    desvios.push((g.get(a, j) - g.get(b, j)).abs());
                }
            }
        }
        let q = quantil(&desvios, 0.10);
        let mut p = quantil(&desvios, 0.90);
        if p <= q {
            p = q + 1e-9;
        }
        let media = desvios.iter().sum::<f64>() / desvios.len().max(1) as f64;
        let var = desvios.iter().map(|d| (d - media).powi(2)).sum::<f64>()
            / desvios.len().max(1) as f64;
        qs[j] = q;
        ps[j] = p;
        ss[j] = var.sqrt().max(1e-9);
    }

    let mut phi_mais = vec![0.0; m];
    let mut phi_menos = vec![0.0; m];
    for a in 0..m {
        for b in 0..m {
            if a == b {
                continue;
            }
            let mut pi = 0.0;
            for j in 0..k {
                pi += w[j] * funcao.avaliar(g.get(a, j) - g.get(b, j), qs[j], ps[j], ss[j]);
            }
            phi_mais[a] += pi;
            phi_menos[b] += pi;
        }
    }
    let denom = if m > 1 { (m - 1) as f64 } else { 1.0 };
    Ok((0..m).map(|i| (phi_mais[i] - phi_menos[i]) / denom).collect())
}

// ===========================================================================
// MAUT — Keeney & Raiffa (1976).
// ===========================================================================

/// Utilidade aditiva com utilidade exponencial: r > 0 => aversão a risco.
pub fn maut(x: &Matriz, w: &[f64], direcoes: &[Direcao], aversao: f64) -> Result<Vec<f64>, String> {
    let w = normalizar_pesos(w, x.colunas)?;
    let g = orientar(x, direcoes)?;
    let denom = 1.0 - (-aversao).exp();
    Ok((0..g.linhas)
        .map(|i| {
            (0..g.colunas)
                .map(|j| {
                    let z = g.get(i, j);
                    let u = if aversao.abs() < 1e-12 {
                        z
                    } else {
                        (1.0 - (-aversao * z).exp()) / denom
                    };
                    u * w[j]
                })
                .sum()
        })
        .collect())
}

// ===========================================================================
// MCDA-C — Ensslin, Montibeller & Noronha (2001).
// ===========================================================================

/// Função de valor ancorada: V = 0 no nível Neutro, V = 100 no nível Bom.
///
/// É a única saída do motor com significado ABSOLUTO: V < 0 é comprometedor,
/// 0..100 é competitivo, V > 100 é excelência. As demais são relativas ao
/// conjunto comparado.
pub fn mcda_c(
    x: &Matriz,
    w: &[f64],
    direcoes: &[Direcao],
    q_neutro: f64,
    q_bom: f64,
) -> Result<Vec<f64>, String> {
    let w = normalizar_pesos(w, x.colunas)?;
    let mut v = Matriz::nova(x.linhas, x.colunas);
    for j in 0..x.colunas {
        let col = x.coluna(j);
        let (neutro, bom) = if direcoes[j] == Direcao::Beneficio {
            (quantil(&col, q_neutro), quantil(&col, q_bom))
        } else {
            (quantil(&col, 1.0 - q_neutro), quantil(&col, 1.0 - q_bom))
        };
        let span = bom - neutro;
        for i in 0..x.linhas {
            v.set(i, j, if span != 0.0 { 100.0 * (col[i] - neutro) / span } else { 0.0 });
        }
    }
    Ok((0..v.linhas)
        .map(|i| (0..v.colunas).map(|j| v.get(i, j) * w[j]).sum())
        .collect())
}

// ===========================================================================
// VIKOR — Opricovic (1979); Opricovic & Tzeng (2002, 2004, 2007).
// Formulação conforme Keunecke, Hein & Kroenke (FURB).
// ===========================================================================

#[derive(Debug, Clone)]
pub struct SaidaVikor {
    /// −Q (maior é melhor, para compor com os demais métodos).
    pub score: Vec<f64>,
    pub s: Vec<f64>,
    pub r: Vec<f64>,
    pub q: Vec<f64>,
    pub c1_vantagem_aceitavel: bool,
    pub c2_estabilidade_aceitavel: bool,
    pub conjunto_compromisso: Vec<usize>,
}

/// Solução de compromisso VIKOR, com as condições C1 e C2.
///
/// S é a utilidade do GRUPO (soma ponderada: aceita compensação) e R o
/// arrependimento INDIVIDUAL máximo (minimax: recusa compensação). Quando os dois
/// discordam, a decisão tem um ponto cego — e é isso que C1/C2 reportam.
pub fn vikor(x: &Matriz, w: &[f64], direcoes: &[Direcao], v: f64) -> Result<SaidaVikor, String> {
    let w = normalizar_pesos(w, x.colunas)?;
    let g = orientar(x, direcoes)?;
    let m = g.linhas;

    let mut s = vec![0.0; m];
    let mut r = vec![0.0f64; m];
    for i in 0..m {
        for j in 0..g.colunas {
            let pen = w[j] * (1.0 - g.get(i, j));
            s[i] += pen;
            r[i] = r[i].max(pen);
        }
    }
    let s_min = s.iter().cloned().fold(f64::INFINITY, f64::min);
    let s_max = s.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let r_min = r.iter().cloned().fold(f64::INFINITY, f64::min);
    let r_max = r.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let ds = if s_max > s_min { s_max - s_min } else { 1.0 };
    let dr = if r_max > r_min { r_max - r_min } else { 1.0 };

    let q: Vec<f64> = (0..m)
        .map(|i| v * (s[i] - s_min) / ds + (1.0 - v) * (r[i] - r_min) / dr)
        .collect();

    let mut ordem: Vec<usize> = (0..m).collect();
    ordem.sort_by(|&a, &b| q[a].partial_cmp(&q[b]).unwrap_or(std::cmp::Ordering::Equal));
    let melhor = ordem[0];
    let segundo = if m > 1 { ordem[1] } else { melhor };
    let dq = if m > 1 { 1.0 / (m - 1) as f64 } else { 0.0 };

    let c1 = q[segundo] - q[melhor] >= dq;
    let idx_min_s = (0..m).min_by(|&a, &b| s[a].partial_cmp(&s[b]).unwrap()).unwrap();
    let idx_min_r = (0..m).min_by(|&a, &b| r[a].partial_cmp(&r[b]).unwrap()).unwrap();
    let c2 = melhor == idx_min_s || melhor == idx_min_r;

    let conjunto = if c1 && c2 {
        vec![melhor]
    } else if !c2 {
        vec![melhor, segundo]
    } else {
        ordem.iter().cloned().filter(|&i| q[i] - q[melhor] < dq).collect()
    };

    Ok(SaidaVikor {
        score: q.iter().map(|x| -x).collect(),
        s,
        r,
        q,
        c1_vantagem_aceitavel: c1,
        c2_estabilidade_aceitavel: c2,
        conjunto_compromisso: conjunto,
    })
}

// ===========================================================================
// TODIM — Gomes & Lima (1992); Gomes (2004); Kahneman & Tversky (1979).
// Via Silva, Rangel & Neves (AMAN/EEIMVR-UFF), TODIM-FSE.
// ===========================================================================

/// Devolve ξ ∈ [0,1]: a melhor alternativa vale exatamente 1, a pior exatamente 0.
///
/// θ é o fator de atenuação de perdas. A assimetria ganho/perda da Teoria dos
/// Prospectos é justamente o que a soma ponderada clássica ignora: uma perda dói
/// mais do que o ganho equivalente agrada.
pub fn todim(x: &Matriz, w: &[f64], direcoes: &[Direcao], theta: f64) -> Result<Vec<f64>, String> {
    if theta <= 0.0 {
        return Err("TODIM: o fator de atenuação θ deve ser positivo".into());
    }
    let w = normalizar_pesos(w, x.colunas)?;
    let g = orientar(x, direcoes)?;
    let m = g.linhas;
    let k = g.colunas;

    let w_max = w.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let wr: Vec<f64> = w.iter().map(|x| x / w_max).collect();
    let soma_w: f64 = wr.iter().sum();

    let mut soma_delta = vec![0.0; m];
    for i in 0..m {
        for j in 0..m {
            if i == j {
                continue;
            }
            let mut total = 0.0;
            for c in 0..k {
                let d = g.get(i, c) - g.get(j, c);
                if d > 0.0 {
                    total += (wr[c] * d / soma_w).sqrt();
                } else if d < 0.0 {
                    total -= (soma_w * (-d) / wr[c]).sqrt() / theta;
                }
            }
            soma_delta[i] += total;
        }
    }
    let lo = soma_delta.iter().cloned().fold(f64::INFINITY, f64::min);
    let hi = soma_delta.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    Ok(soma_delta
        .iter()
        .map(|d| if hi <= lo { 0.5 } else { (d - lo) / (hi - lo) })
        .collect())
}

// ===========================================================================
// SAPEVO-M — Gomes et al. (1997); Teixeira, Santos & Gomes (SPOLM/CASNAV, 2019).
// ===========================================================================

/// Substituto do peso nulo: 1% do valor imediatamente superior.
/// Faz parte do método — "não faz sentido que um critério possua peso nulo".
pub const FRACAO_PESO_MINIMO: f64 = 0.01;

/// Banda proporcional da fuzzificação: x → (x(1−α), x, x(1+α)).
/// Espelha `FUZZY_ALPHA` do `config.py`. Os dois precisam andar juntos: um motor
/// com α diferente do outro produz divergência que PARECE erro de algoritmo.
pub const FUZZY_ALPHA: f64 = 0.10;

/// Normalização do SAPEVO-M, incluindo o tratamento do peso nulo.
pub fn normalizar_sapevo(v: &[f64]) -> Vec<f64> {
    let lo = v.iter().cloned().fold(f64::INFINITY, f64::min);
    let hi = v.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let mut vn: Vec<f64> = if hi <= lo {
        vec![0.5; v.len()]
    } else {
        v.iter().map(|x| (x - lo) / (hi - lo)).collect()
    };
    let menor_positivo = vn.iter().cloned().filter(|&x| x > 0.0).fold(f64::INFINITY, f64::min);
    if menor_positivo.is_finite() {
        for x in vn.iter_mut() {
            if *x <= 0.0 {
                *x = menor_positivo * FRACAO_PESO_MINIMO;
            }
        }
    } else {
        let n = vn.len() as f64;
        vn.iter_mut().for_each(|x| *x = 1.0 / n);
    }
    vn
}

/// Pesos dos critérios a partir dos julgamentos ordinais de VÁRIOS decisores.
///
/// Cada matriz usa a escala de sete pontos {-3,-2,-1,0,1,2,3}. Os vetores de
/// preferência são somados ANTES de normalizar: é o que dispensa a pré-ordem de
/// consenso entre decisores, e é o que distingue o SAPEVO-M do SAPEVO original.
pub fn sapevo_m_pesos(matrizes: &[Matriz]) -> Result<Vec<f64>, String> {
    if matrizes.is_empty() {
        return Err("SAPEVO-M: nenhum decisor informado".into());
    }
    let n = matrizes[0].linhas;
    if matrizes.iter().any(|m| !m.quadrada() || m.linhas != n) {
        return Err("SAPEVO-M: todos os decisores devem julgar os mesmos critérios".into());
    }
    let mut v = vec![0.0; n];
    for m in matrizes {
        for i in 0..n {
            v[i] += (0..n).map(|j| m.get(i, j)).sum::<f64>();
        }
    }
    let pesos = normalizar_sapevo(&v);
    let soma: f64 = pesos.iter().sum();
    Ok(pesos.iter().map(|x| x / soma).collect())
}

/// SAPEVO-M adaptado a uma matriz de decisão CARDINAL.
///
/// O método nasceu para julgamentos ORDINAIS; aqui as comparações par a par são
/// derivadas do desempenho observado e discretizadas na escala de sete pontos
/// {-3..3}. É uma ADAPTAÇÃO deste projeto, não o método como publicado — a forma
/// fiel, com julgamento de decisores, é `sapevo_m_pesos`.
///
/// Espelha `metodos_br.sapevo_m_de_matriz`. Existe para que a verificação cruzada
/// cubra os dez métodos: até a versão anterior o SAPEVO-M não tinha contraparte
/// em Rust e passava despercebido pelo comparador. Ver bugs.md #BUG-041.
pub fn sapevo_m_de_matriz(
    x: &Matriz,
    w: &[f64],
    direcoes: &[Direcao],
) -> Result<Vec<f64>, String> {
    let w = normalizar_pesos(w, x.colunas)?;
    let g = orientar(x, direcoes)?;
    let (m, k) = (g.linhas, g.colunas);
    let mut mat = Matriz::nova(m, k);
    for j in 0..k {
        let mut soma = vec![0.0; m];
        for a in 0..m {
            for b in 0..m {
                if a == b {
                    continue;
                }
                // round-half-away-from-zero, como o np.round do NumPy NÃO faz:
                // o NumPy usa banker's rounding. A diferença só aparece em .5
                // exato, que aqui vem de diferenças como 1/6 — por isso o
                // arredondamento é replicado explicitamente, não aproximado.
                let d = (g.get(a, j) - g.get(b, j)) * 3.0;
                let r = arredondar_par(d);
                soma[a] += r.clamp(-3.0, 3.0);
            }
        }
        let coluna = normalizar_sapevo(&soma);
        for a in 0..m {
            mat.set(a, j, coluna[a]);
        }
    }
    Ok((0..m)
        .map(|a| (0..k).map(|j| mat.get(a, j) * w[j]).sum())
        .collect())
}

/// Arredondamento para o par mais próximo (banker's rounding), igual ao `np.round`.
///
/// `f64::round` do Rust arredonda 0,5 para longe do zero; o NumPy arredonda para o
/// par. Com `0.5 → 1` em vez de `0.5 → 0`, um grau do SAPEVO muda e o ranking pode
/// virar. Replicar a regra é o que mantém os dois motores comparáveis.
fn arredondar_par(x: f64) -> f64 {
    let r = x.round();
    // Comparação EXATA com 0,5 — sem tolerância, de propósito.
    //
    // 0,5 é representável exatamente em binário, e a regra do par só vale para o
    // empate exato. A primeira versão usava `< 1e-12`, e isso capturava valores
    // como 1,4999999999999998 — que `round()` já havia levado para 1 — para
    // subtrair 1 de novo, devolvendo 0. Um grau do SAPEVO mudava de 1 para 0 em
    // 22 dos 38 casos. Ver bugs.md #BUG-042.
    if x.fract().abs() == 0.5 && (r % 2.0) != 0.0 {
        r - x.signum()
    } else {
        r
    }
}

// ===========================================================================
// TOPSIS Fuzzy — Chen (2000).
// ===========================================================================

/// TOPSIS Fuzzy com números triangulares (l, m, u), conforme Chen (2000).
///
/// A matriz crisp é fuzzificada com banda PROPORCIONAL ±alpha e normalizada de
/// forma linear; os ideais são ABSOLUTOS — (1,1,1) e (0,0,0). São três escolhas
/// distintas das do `topsis_2n` (normalização vetorial, ideais relativos), e por
/// isso os dois podem divergir: é diferença de método, não erro.
///
/// No critério de CUSTO os extremos trocam de lado — o maior u vira o menor l —,
/// e é por isso que o `l` do resultado divide pelo `u` da entrada. Normalizar
/// componente a componente sem a troca produz um triângulo invertido que continua
/// parecendo válido.
pub fn fuzzy_topsis(
    x: &Matriz,
    w: &[f64],
    direcoes: &[Direcao],
    alpha: f64,
) -> Result<Vec<f64>, String> {
    if alpha < 0.0 {
        return Err("TOPSIS Fuzzy: alpha deve ser ≥ 0".into());
    }
    let w = normalizar_pesos(w, x.colunas)?;
    if direcoes.len() != x.colunas {
        return Err("TOPSIS Fuzzy: direções incompatíveis com a matriz".into());
    }
    let (m, k) = (x.linhas, x.colunas);

    // Fuzzificação: x → (x(1−α), x, x(1+α)), ordenada (valores negativos trocam).
    let mut tri = vec![[0.0f64; 3]; m * k];
    for i in 0..m {
        for j in 0..k {
            let v = x.get(i, j);
            let mut t = [v * (1.0 - alpha), v, v * (1.0 + alpha)];
            t.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
            tri[i * k + j] = t;
        }
    }

    // Translação das colunas não-positivas, igual ao lado Python.
    //
    // A normalização de Chen é multiplicativa e só é definida para dados > 0. Com
    // l⁻ ≤ 0 num critério de custo, as razões invertem a ordem dos vértices e o
    // triângulo sai com l > u. Dados reais têm zero e negativo (VPL negativo,
    // vacância 0%), então a coluna é deslocada por 1% da amplitude acima de zero.
    // A translação preserva ordem e diferenças, mas NÃO as razões — e isso está
    // declarado no relatório. Ver bugs.md #BUG-044.
    for j in 0..k {
        let lo = (0..m).map(|i| tri[i * k + j][0]).fold(f64::INFINITY, f64::min);
        if lo <= 0.0 {
            let hi = (0..m).map(|i| tri[i * k + j][2]).fold(f64::NEG_INFINITY, f64::max);
            let amp = hi - lo;
            let eps = if amp > 0.0 { amp * 0.01 } else { 1.0 };
            let desloc = -lo + eps;
            for i in 0..m {
                for c in 0..3 {
                    tri[i * k + j][c] += desloc;
                }
            }
        }
    }

    // Normalização linear de Chen.
    let mut r = vec![[0.0f64; 3]; m * k];
    for j in 0..k {
        match direcoes[j] {
            Direcao::Beneficio => {
                let upos = (0..m).map(|i| tri[i * k + j][2]).fold(f64::NEG_INFINITY, f64::max);
                let d = if upos == 0.0 { 1.0 } else { upos };
                for i in 0..m {
                    let t = tri[i * k + j];
                    r[i * k + j] = [t[0] / d, t[1] / d, t[2] / d];
                }
            }
            Direcao::Custo => {
                let lneg = (0..m).map(|i| tri[i * k + j][0]).fold(f64::INFINITY, f64::min);
                for i in 0..m {
                    let t = tri[i * k + j];
                    // 1/0 → 0 (e não infinito), igual ao lado Python.
                    let inv = |d: f64| if d == 0.0 { 0.0 } else { lneg / d };
                    r[i * k + j] = [inv(t[2]), inv(t[1]), inv(t[0])];
                }
            }
        }
    }

    // Ponderação, distância vertex aos ideais absolutos e proximidade.
    Ok((0..m)
        .map(|i| {
            let (mut dp, mut dn) = (0.0, 0.0);
            for j in 0..k {
                let v: Vec<f64> = r[i * k + j].iter().map(|c| c * w[j]).collect();
                dp += (v.iter().map(|c| (c - 1.0).powi(2)).sum::<f64>() / 3.0).sqrt();
                dn += (v.iter().map(|c| c * c).sum::<f64>() / 3.0).sqrt();
            }
            let soma = dp + dn;
            if soma == 0.0 { 0.0 } else { dn / soma }
        })
        .collect())
}

// ===========================================================================
// Métodos ordinais — Borda (1781), Copeland (1951).
// Via Gomes Júnior (SPOLM 2008).
// ===========================================================================

/// Contagem de Borda: pontos = (n − posição), somados sobre os julgadores.
pub fn borda(matriz_ranks: &[Vec<usize>], n_alternativas: usize) -> Vec<f64> {
    let mut pontos = vec![0.0; n_alternativas];
    for rk in matriz_ranks {
        for (i, &pos) in rk.iter().enumerate() {
            pontos[i] += (n_alternativas - pos) as f64;
        }
    }
    pontos
}

/// Copeland: vitórias menos derrotas em confrontos diretos.
///
/// Quando Copeland e Borda discordam há um ciclo de maioria (paradoxo de
/// Condorcet) escondido nos dados — a discordância é o achado, não um defeito.
pub fn copeland(matriz_ranks: &[Vec<usize>], n_alternativas: usize) -> Vec<f64> {
    let mut score = vec![0.0; n_alternativas];
    for a in 0..n_alternativas {
        for b in 0..n_alternativas {
            if a == b {
                continue;
            }
            let vitorias = matriz_ranks.iter().filter(|rk| rk[a] < rk[b]).count();
            let derrotas = matriz_ranks.iter().filter(|rk| rk[a] > rk[b]).count();
            if vitorias > derrotas {
                score[a] += 1.0;
            } else if vitorias < derrotas {
                score[a] -= 1.0;
            }
        }
    }
    score
}

// ===========================================================================
// TESTES
// ===========================================================================
#[cfg(test)]
mod testes {
    use super::*;

    fn problema_dominante() -> (Matriz, Vec<Direcao>, Vec<f64>) {
        // alt0 é a melhor nos DOIS critérios (dominância estrita).
        let x = Matriz::de_vec(3, 2, vec![10.0, 1.0, 8.0, 3.0, 6.0, 5.0]).unwrap();
        (x, vec![Direcao::Beneficio, Direcao::Custo], vec![0.5, 0.5])
    }

    #[test]
    fn orientar_inverte_custo_e_neutraliza_constante() {
        let x = Matriz::de_vec(3, 2, vec![1.0, 5.0, 3.0, 5.0, 5.0, 5.0]).unwrap();
        let g = orientar(&x, &[Direcao::Custo, Direcao::Beneficio]).unwrap();
        assert!((g.get(0, 0) - 1.0).abs() < 1e-12);
        assert!((g.get(2, 0) - 0.0).abs() < 1e-12);
        // coluna constante => 0,5 (indiferença), nunca 0.
        for i in 0..3 {
            assert!((g.get(i, 1) - 0.5).abs() < 1e-12);
        }
    }

    #[test]
    fn ahp_recupera_pesos_de_matriz_consistente() {
        let p = [0.5, 0.25, 0.15, 0.10];
        let mut a = Matriz::nova(4, 4);
        for i in 0..4 {
            for j in 0..4 {
                a.set(i, j, p[i] / p[j]);
            }
        }
        let saida = pesos_ahp(&a).unwrap();
        for i in 0..4 {
            assert!((saida.pesos[i] - p[i]).abs() < 1e-9, "peso {i} divergiu");
        }
        assert!((saida.lambda_max - 4.0).abs() < 1e-9);
        assert!(saida.cr < 1e-9 && saida.consistente());
    }

    #[test]
    fn ahp_detecta_ciclo_de_preferencia() {
        // A≫B≫C≫A: inconsistência máxima.
        let a = Matriz::de_vec(
            3, 3,
            vec![1.0, 9.0, 1.0 / 9.0, 1.0 / 9.0, 1.0, 9.0, 9.0, 1.0 / 9.0, 1.0],
        ).unwrap();
        let saida = pesos_ahp(&a).unwrap();
        assert!(saida.cr > 0.10, "CR = {} deveria reprovar", saida.cr);
        assert!(!saida.consistente());
    }

    #[test]
    fn dematel_pesos_somam_um_e_papeis_conferem() {
        let z = Matriz::de_vec(
            4, 4,
            vec![0.0, 3.0, 3.0, 0.0,
                 0.0, 0.0, 2.0, 0.0,
                 0.0, 0.0, 0.0, 0.0,
                 3.0, 3.0, 3.0, 0.0],
        ).unwrap();
        let s = dematel(&z).unwrap();
        let soma: f64 = s.pesos.iter().sum();
        assert!((soma - 1.0).abs() < 1e-12);
        assert!(s.eh_causa(3), "critério 4 influencia todos: deve ser CAUSA");
        assert!(!s.eh_causa(2), "critério 3 não influencia ninguém: deve ser EFEITO");
    }

    #[test]
    fn todos_os_metodos_elegem_a_alternativa_dominante() {
        let (x, d, w) = problema_dominante();
        let checagens: Vec<(&str, Vec<f64>)> = vec![
            ("TOPSIS 2N", topsis_2n(&x, &w, &d).unwrap()),
            ("ELECTRE I", electre_i(&x, &w, &d, 0.65, 0.35).unwrap().score),
            ("ELECTRE II", electre_ii(&x, &w, &d, 0.75, 0.60, 0.25, 0.40).unwrap().score),
            ("PROMETHEE II", promethee_ii(&x, &w, &d, FuncaoPreferencia::Linear).unwrap()),
            ("MAUT", maut(&x, &w, &d, 2.0).unwrap()),
            ("MCDA-C", mcda_c(&x, &w, &d, 0.25, 0.75).unwrap()),
            ("VIKOR", vikor(&x, &w, &d, 0.5).unwrap().score),
            ("TODIM", todim(&x, &w, &d, 1.0).unwrap()),
        ];
        for (nome, score) in checagens {
            let rk = ranks(&score);
            assert_eq!(rk[0], 1, "{nome} não elegeu a alternativa dominante: {rk:?}");
            assert_eq!(rk[2], 3, "{nome} não pôs a pior em último: {rk:?}");
        }
    }

    #[test]
    fn vikor_q_da_melhor_e_zero_e_condicoes_sao_avaliadas() {
        let (x, d, w) = problema_dominante();
        let s = vikor(&x, &w, &d, 0.5).unwrap();
        assert!(s.q[0].abs() < 1e-12, "Q da melhor deve ser 0, veio {}", s.q[0]);
        assert!(s.c1_vantagem_aceitavel && s.c2_estabilidade_aceitavel);
        assert_eq!(s.conjunto_compromisso, vec![0]);
    }

    #[test]
    fn todim_normaliza_entre_zero_e_um_em_qualquer_theta() {
        let (x, d, w) = problema_dominante();
        for theta in [0.5, 1.0, 2.5] {
            let xi = todim(&x, &w, &d, theta).unwrap();
            let hi = xi.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
            let lo = xi.iter().cloned().fold(f64::INFINITY, f64::min);
            assert!((hi - 1.0).abs() < 1e-12 && lo.abs() < 1e-12, "θ={theta}");
        }
        assert!(todim(&x, &w, &d, 0.0).is_err(), "θ=0 deve ser rejeitado");
    }

    #[test]
    fn sapevo_m_nao_produz_peso_nulo() {
        // 3 decisores, 4 critérios, ordem de importância decrescente.
        let d1 = Matriz::de_vec(4, 4, vec![
            0.0, 1.0, 2.0, 3.0, -1.0, 0.0, 1.0, 2.0,
            -2.0, -1.0, 0.0, 1.0, -3.0, -2.0, -1.0, 0.0]).unwrap();
        let d2 = Matriz::de_vec(4, 4, vec![
            0.0, 2.0, 2.0, 3.0, -2.0, 0.0, 1.0, 1.0,
            -2.0, -1.0, 0.0, 2.0, -3.0, -1.0, -2.0, 0.0]).unwrap();
        let p = sapevo_m_pesos(&[d1, d2]).unwrap();
        assert!((p.iter().sum::<f64>() - 1.0).abs() < 1e-12);
        assert!(p.iter().all(|&x| x > 0.0), "nenhum peso pode ser nulo: {p:?}");
        assert!(p[0] > p[1] && p[1] > p[2] && p[2] > p[3], "ordem não preservada");
    }

    #[test]
    fn copeland_empata_em_ciclo_de_condorcet() {
        // A>B>C, C>A>B, B>C>A  => ciclo de maioria perfeito.
        let rk = vec![vec![1, 2, 3], vec![3, 1, 2], vec![2, 3, 1]];
        let c = copeland(&rk, 3);
        assert!(c.iter().all(|&x| x == 0.0), "ciclo deve empatar tudo em 0: {c:?}");
    }

    #[test]
    fn ranks_e_estavel_em_empates() {
        assert_eq!(ranks(&[1.0, 1.0, 1.0]), vec![1, 2, 3]);
        assert_eq!(ranks(&[3.0, 1.0, 2.0]), vec![1, 3, 2]);
    }

    #[test]
    fn quantil_bate_com_numpy() {
        let v = vec![1.0, 2.0, 3.0, 4.0];
        assert!((quantil(&v, 0.0) - 1.0).abs() < 1e-12);
        assert!((quantil(&v, 0.5) - 2.5).abs() < 1e-12);
        assert!((quantil(&v, 0.25) - 1.75).abs() < 1e-12);
        assert!((quantil(&v, 1.0) - 4.0).abs() < 1e-12);
    }

    #[test]
    fn resolver_sistema_linear() {
        let a = Matriz::de_vec(2, 2, vec![2.0, 1.0, 1.0, 3.0]).unwrap();
        let b = Matriz::de_vec(2, 1, vec![5.0, 10.0]).unwrap();
        let x = resolver(&a, &b).unwrap();
        assert!((x.get(0, 0) - 1.0).abs() < 1e-12);
        assert!((x.get(1, 0) - 3.0).abs() < 1e-12);
    }

    #[test]
    fn pesos_invalidos_sao_rejeitados() {
        assert!(normalizar_pesos(&[1.0, -1.0], 2).is_err());
        assert!(normalizar_pesos(&[0.0, 0.0], 2).is_err());
        assert!(normalizar_pesos(&[1.0], 2).is_err());
    }
}

#[cfg(test)]
mod testes_sapevo_fuzzy {
    use super::*;

    fn caso() -> (Matriz, Vec<Direcao>, Vec<f64>) {
        let mut x = Matriz::nova(4, 3);
        let d = [[25.0, 40.0, 4.2], [15.0, 35.0, 3.5], [5.0, 40.0, 8.8], [25.0, 30.0, 2.5]];
        for i in 0..4 { for j in 0..3 { x.set(i, j, d[i][j]); } }
        (x, vec![Direcao::Beneficio, Direcao::Beneficio, Direcao::Custo], vec![0.5, 0.3, 0.2])
    }

    #[test]
    fn sapevo_cardinal_bate_com_python() {
        let (x, dirs, w) = caso();
        let s = sapevo_m_de_matriz(&x, &w, &dirs).unwrap();
        // Valores MEDIDOS em metodos_br.sapevo_m_de_matriz(X, dirs, w), 12 casas.
        // A primeira versão deste teste trazia números escritos de cabeça, e o
        // teste "pegou" um defeito que não existia. Valor esperado de teste se
        // calcula na implementação de referência — nunca se estima.
        let esperado = [0.950000000000, 0.552564102564, 0.303807692308, 0.701384615385];
        for (a, b) in s.iter().zip(esperado.iter()) {
            assert!((a - b).abs() < 1e-9, "SAPEVO: {:?} != {:?}", s, esperado);
        }
    }

    #[test]
    fn fuzzy_topsis_bate_com_python() {
        let (x, dirs, w) = caso();
        let s = fuzzy_topsis(&x, &w, &dirs, 0.10).unwrap();
        // Medidos em fuzzy.fuzzy_topsis_de_crisp(X, w, dirs), alpha = 0,10.
        let esperado = [0.278894906636, 0.214113302841, 0.138751836800, 0.280626003534];
        for (a, b) in s.iter().zip(esperado.iter()) {
            assert!((a - b).abs() < 1e-8, "TOPSIS Fuzzy: {:?} != {:?}", s, esperado);
        }
    }

    #[test]
    fn arredondamento_segue_o_numpy() {
        for (x, esp) in [(0.5, 0.0), (1.5, 2.0), (2.5, 2.0), (-0.5, 0.0), (-2.5, -2.0),
                         (3.5, 4.0), (-1.5, -2.0), (1.2, 1.0), (-1.2, -1.0)] {
            assert_eq!(arredondar_par(x), esp, "arredondar_par({x})");
        }
        // Quase-empates: NÃO são empate, e a regra do par não se aplica a eles.
        // Era exatamente aqui que a tolerância de 1e-12 errava (#BUG-042).
        for (x, esp) in [(1.4999999999999998, 1.0), (0.4999999999999999, 0.0),
                         (2.5000000000000004, 3.0), (-1.4999999999999998, -1.0)] {
            assert_eq!(arredondar_par(x), esp, "quase-empate arredondar_par({x})");
        }
    }
}
