const SHIKI_URL = "https://esm.sh/shiki@4.6.0";

const GRAMMARS = {
    aergia: "assets/grammars/aergia.tmLanguage.json"
};

const THEME = {
    name: "las-r-dark",
    type: "dark",
    colors: {
        "editor.background": "#242424",
        "editor.foreground": "#e6e6ed"
    },
    settings: [
        { settings: { foreground: "#e6e6ed", background: "#242424" } },
        { scope: ["comment"], settings: { foreground: "#929292", fontStyle: "italic" } },
        { scope: ["string", "punctuation.definition.string"], settings: { foreground: "#b5d99c" } },
        { scope: ["constant.character.escape"], settings: { foreground: "#e8ce9a" } },
        { scope: ["constant.numeric", "constant.language"], settings: { foreground: "#a8c9ff" } },
        { scope: ["keyword", "storage", "keyword.control", "keyword.other"], settings: { foreground: "#dfadff" } },
        { scope: ["keyword.operator", "punctuation"], settings: { foreground: "#c5c5d0" } },
        { scope: ["variable.language"], settings: { foreground: "#dfadff" } },
        { scope: ["variable.parameter"], settings: { foreground: "#e8ce9a" } },
        { scope: ["variable", "variable.other"], settings: { foreground: "#80cfe0" } },
        { scope: ["variable.other.definition", "entity.name.function"], settings: { foreground: "#adadff" } },
        { scope: ["support.function", "support.type", "support.class"], settings: { foreground: "#adadff" } },
        { scope: ["entity.name.type", "entity.name.class"], settings: { foreground: "#e8ce9a" } },
        { scope: ["invalid"], settings: { foreground: "#ff7777" } }
    ]
};

function langOf(el) {
    const m = el.className.match(/language-([\w+-]+)/);
    return m ? m[1].toLowerCase() : null;
}

function isCustom(lang) {
    return lang !== null && Object.prototype.hasOwnProperty.call(GRAMMARS, lang);
}

function wrapBare() {
    document.querySelectorAll("pre > code[class*='language-']").forEach(function (code) {
        const lang = langOf(code);
        const pre = code.parentElement;
        if (!isCustom(lang) || pre.closest("div.highlighter-rouge")) return;

        const block = document.createElement("div");
        const holder = document.createElement("div");
        block.className = "language-" + lang + " highlighter-rouge";
        holder.className = "highlight";
        pre.classList.add("highlight");

        pre.replaceWith(block);
        holder.appendChild(pre);
        block.appendChild(holder);
    });
}

async function run() {
    const blocks = Array.from(document.querySelectorAll("div.highlighter-rouge"))
        .filter(function (b) { return isCustom(langOf(b)); });

    if (!blocks.length) return;

    const base = document.documentElement.dataset.baseurl || "";
    const needed = Array.from(new Set(blocks.map(langOf)));

    const [{ createHighlighter }, grammars] = await Promise.all([
        import(SHIKI_URL),
        Promise.all(needed.map(function (lang) {
            return fetch(base + "/" + GRAMMARS[lang])
                .then(function (r) { return r.json(); })
                .then(function (g) { return Object.assign({}, g, { name: lang }); });
        }))
    ]);

    const hl = await createHighlighter({ themes: [THEME], langs: grammars });

    blocks.forEach(function (block) {
        const holder = block.querySelector(".highlight");
        const code = block.querySelector("code");
        if (!holder || !code) return;

        holder.innerHTML = hl.codeToHtml(code.textContent.replace(/\n$/, ""), {
            lang: langOf(block),
            theme: THEME.name
        });
    });
}

wrapBare();

run().catch(function (err) {
    console.warn("Syntax highlighting unavailable:", err);
});