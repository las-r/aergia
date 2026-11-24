document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("menu-toggle");
    if (toggle) {
        toggle.addEventListener("click", function () {
            const open = document.body.classList.toggle("sidebar-open");
            toggle.setAttribute("aria-expanded", String(open));
        });
    }

    document.querySelectorAll("div.highlighter-rouge").forEach(function (block) {
        const pre = block.querySelector("pre");
        if (!pre || !navigator.clipboard) return;

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "copy-btn";
        btn.textContent = "Copy";

        btn.addEventListener("click", function () {
            const pre = block.querySelector("pre");
            navigator.clipboard.writeText(pre.innerText.replace(/\n$/, "")).then(function () {
                btn.textContent = "Copied";
                setTimeout(function () { btn.textContent = "Copy"; }, 1500);
            });
        });

        block.appendChild(btn);
    });

    const input = document.getElementById("search-input");
    const results = document.getElementById("search-results");
    if (!input || !results) return;

    let index = null;
    let loading = null;
    let selected = -1;

    function load() {
        if (index) return Promise.resolve(index);
        if (!loading) {
            loading = fetch(input.dataset.searchUrl)
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    index = data.map(function (d) {
                        return {
                            title: d.title,
                            section: d.section,
                            url: d.url,
                            content: d.content,
                            lowerTitle: d.title.toLowerCase(),
                            lowerContent: d.content.toLowerCase()
                        };
                    });
                    return index;
                })
                .catch(function () { loading = null; index = []; return index; });
        }
        return loading;
    }

    function score(doc, terms) {
        let total = 0;
        for (const t of terms) {
            let s = 0;
            if (doc.lowerTitle.includes(t)) s += 10;
            if (doc.lowerContent.includes(t)) s += 1;
            if (s === 0) return 0;
            total += s;
        }
        return total;
    }

    function snippet(doc, terms) {
        const pos = doc.lowerContent.indexOf(terms[0]);
        if (pos < 0) return doc.section || "";
        const start = Math.max(0, pos - 30);
        const text = doc.content.slice(start, start + 90).trim();
        return (start > 0 ? "..." : "") + text + "...";
    }

    function render(matches, terms) {
        results.innerHTML = "";
        selected = -1;

        if (!matches.length) {
            const li = document.createElement("li");
            li.className = "search-empty";
            li.textContent = "No results";
            results.appendChild(li);
        }

        matches.forEach(function (doc) {
            const li = document.createElement("li");
            const a = document.createElement("a");
            const small = document.createElement("small");

            a.href = doc.url;
            a.textContent = doc.title;
            small.textContent = snippet(doc, terms);

            a.appendChild(small);
            li.appendChild(a);
            results.appendChild(li);
        });

        results.hidden = false;
    }

    function run() {
        const terms = input.value.toLowerCase().split(/\s+/).filter(Boolean);
        if (!terms.length) { results.hidden = true; return; }

        load().then(function (docs) {
            const matches = docs
                .map(function (d) { return { d: d, s: score(d, terms) }; })
                .filter(function (m) { return m.s > 0; })
                .sort(function (a, b) { return b.s - a.s; })
                .slice(0, 8)
                .map(function (m) { return m.d; });
            render(matches, terms);
        });
    }

    function move(delta) {
        const items = results.querySelectorAll("a");
        if (!items.length) return;
        if (selected >= 0) items[selected].classList.remove("selected");
        selected = (selected + delta + items.length) % items.length;
        items[selected].classList.add("selected");
        items[selected].scrollIntoView({ block: "nearest" });
    }

    input.addEventListener("focus", load);
    input.addEventListener("input", run);

    input.addEventListener("keydown", function (e) {
        if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
        else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
        else if (e.key === "Enter") {
            const items = results.querySelectorAll("a");
            const target = items[selected >= 0 ? selected : 0];
            if (target) window.location.href = target.href;
        }
        else if (e.key === "Escape") { results.hidden = true; input.blur(); }
    });

    document.addEventListener("click", function (e) {
        if (!e.target.closest(".search")) results.hidden = true;
    });

    document.addEventListener("keydown", function (e) {
        const tag = document.activeElement && document.activeElement.tagName;
        if (e.key === "/" && tag !== "INPUT" && tag !== "TEXTAREA") {
            e.preventDefault();
            input.focus();
        }
    });
});