import math

import pytest

from cotejo.detectores import Modelos, detectar

try:
    import torch
except ImportError:
    torch = None
requiere_torch = pytest.mark.skipif(torch is None, reason="torch no instalado")


@requiere_torch
def test_fast_detectgpt_analitico_contra_muestreo():
    from cotejo.detectores import fast_detectgpt
    g = torch.Generator().manual_seed(0)
    lr = torch.randn(1, 12, 7, generator=g)
    ls = torch.randn(1, 12, 7, generator=g)
    y = torch.randint(0, 7, (1, 12), generator=g)
    analitico = fast_detectgpt(lr, ls, y)
    lp = torch.log_softmax(ls, -1)
    muestras = torch.distributions.Categorical(logits=lr).sample((40000,))  # (S, 1, 12)
    ll_x = lp.gather(-1, y.unsqueeze(-1)).squeeze(-1).sum()
    ll_m = lp[0].gather(-1, muestras[:, 0, :].T).sum(0)  # (S,)
    muestreo = float((ll_x - ll_m.mean()) / ll_m.std())
    assert analitico == pytest.approx(muestreo, abs=0.05)


@requiere_torch
def test_binoculars_igual_modelo_es_perplejidad_sobre_entropia():
    from cotejo.detectores import binoculars
    g = torch.Generator().manual_seed(1)
    lo = torch.randn(1, 6, 5, generator=g)
    ids = torch.randint(0, 5, (1, 6), generator=g)
    p = torch.softmax(lo[0], -1)
    ppl = -sum(math.log(p[i, ids[0, i + 1]]) for i in range(5)) / 5
    ent = float(-(p * p.log()).sum(-1).mean())
    assert binoculars(lo, lo, ids) == pytest.approx(ppl / ent, rel=1e-5)


@pytest.fixture
def modelos_diminutos(extr):
    transformers = pytest.importorskip("transformers")
    tokenizers = pytest.importorskip("tokenizers")
    palabras = sorted({p[0].lower() for s in extr["segmentos"] for p in s["palabras"]})
    vocab = {"[UNK]": 0, **{w: i + 1 for i, w in enumerate(palabras)}}
    tk = tokenizers.Tokenizer(tokenizers.models.WordLevel(vocab, unk_token="[UNK]"))
    tk.normalizer = tokenizers.normalizers.Lowercase()
    tk.pre_tokenizer = tokenizers.pre_tokenizers.Whitespace()
    tok = transformers.PreTrainedTokenizerFast(tokenizer_object=tk, unk_token="[UNK]")
    mods = []
    for semilla in (0, 1):
        torch.manual_seed(semilla)
        cfg = transformers.GPT2Config(vocab_size=len(vocab), n_positions=64, n_embd=16, n_layer=1, n_head=2)
        mods.append(transformers.GPT2LMHeadModel(cfg).eval())
    return Modelos(tok, mods[0], mods[1], ("diminuto-a", "diminuto-b"))


@requiere_torch
def test_detectar_con_modelo_diminuto_y_referencia(extr, modelos_diminutos, tmp_path):
    for grupo, n in (("humano", 3), ("generado", 2)):
        (tmp_path / "ref" / grupo).mkdir(parents=True)
        for k in range(n):
            (tmp_path / "ref" / grupo / f"{k}.txt").write_text(
                "los sistemas de memoria transactiva distribuyen el conocimiento entre los miembros\n\n"
                f"las redes neuronales profundas aprenden representaciones {k}", encoding="utf-8")
    det = detectar(extr, modelos_diminutos, tmp_path / "ref", min_palabras=5, max_tokens=64,
                   avisar=lambda *_: None)
    assert det["disponible"] and det["parrafos"]
    p = det["parrafos"][0]
    assert p["binoculars"] > 0 and math.isfinite(p["fast_detectgpt"])
    assert 0 <= p["pos_binoculars_humano"] <= 100
    assert det["referencia"]["grupos"]["humano"]["parrafos"] == 6
    assert {s["seccion"] for s in det["secciones"]} >= {"Introducción"}
    assert "aviso_referencia" in det and det["aviso_referencia"] is None


@requiere_torch
def test_sin_referencia_avisa(extr, modelos_diminutos):
    det = detectar(extr, modelos_diminutos, None, min_palabras=5, max_tokens=64, avisar=lambda *_: None)
    assert "no se interpreta" in det["aviso_referencia"]


def test_sin_modelos(extr):
    det = detectar(extr, None, motivo="sin torch")
    assert det["disponible"] is False and det["motivo"] == "sin torch" and det["limitaciones"]


@requiere_torch
def test_cargar_desde_disco(modelos_diminutos, tmp_path):
    for nombre, m in (("a", modelos_diminutos.base), ("b", modelos_diminutos.instruct)):
        m.save_pretrained(tmp_path / nombre)
        modelos_diminutos.tok.save_pretrained(tmp_path / nombre)
    cargados = Modelos.cargar(str(tmp_path / "a"), str(tmp_path / "b"), "cpu")
    r = cargados.puntuar("los sistemas de memoria transactiva distribuyen el conocimiento")
    esperado = modelos_diminutos.puntuar("los sistemas de memoria transactiva distribuyen el conocimiento")
    assert r["binoculars"] == pytest.approx(esperado["binoculars"], rel=1e-4)


@requiere_torch
def test_tokenizadores_distintos(modelos_diminutos, tmp_path):
    import transformers
    import tokenizers
    modelos_diminutos.base.save_pretrained(tmp_path / "a")
    modelos_diminutos.tok.save_pretrained(tmp_path / "a")
    tk = tokenizers.Tokenizer(tokenizers.models.WordLevel({"[UNK]": 0, "otra": 1}, unk_token="[UNK]"))
    transformers.PreTrainedTokenizerFast(tokenizer_object=tk, unk_token="[UNK]").save_pretrained(tmp_path / "b")
    with pytest.raises(ValueError, match="tokenizador"):
        Modelos.cargar(str(tmp_path / "a"), str(tmp_path / "b"), "cpu")
