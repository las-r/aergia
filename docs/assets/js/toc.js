document.addEventListener("DOMContentLoaded", function () {
    const content = document.querySelector(".doc-content");
    const list = document.getElementById("toc-list");
    const toc = document.getElementById("toc");

    if (!content || !list || !toc) return;

    const links = new Map();

    content.querySelectorAll("h2, h3, h4").forEach(function (heading) {
        if (!heading.id) {
            const base = heading.textContent.trim().toLowerCase()
                .replace(/[^\w\s-]/g, "")
                .replace(/\s+/g, "-");

            let id = base;
            let n = 1;

            while (document.getElementById(id)) {
                id = base + "-" + n++;
            }

            heading.id = id;
        }

        const label = heading.textContent.trim();

        const anchor = document.createElement("a");
        anchor.className = "anchor";
        anchor.href = "#" + heading.id;
        anchor.setAttribute("aria-label", "Link to this section");
        anchor.textContent = "#";
        heading.appendChild(anchor);

        if (heading.tagName === "H4") return;

        const li = document.createElement("li");
        const a = document.createElement("a");

        a.href = "#" + heading.id;
        a.textContent = label;

        if (heading.tagName === "H3") {
            li.classList.add("toc-subitem");
        }

        li.appendChild(a);
        list.appendChild(li);
        links.set(heading, a);
    });

    if (!list.children.length) {
        toc.hidden = true;
        return;
    }

    const headings = Array.from(links.keys());

    function update() {
        let current = headings[0];
        for (const h of headings) {
            if (h.getBoundingClientRect().top <= 80) current = h;
            else break;
        }
        links.forEach(function (a, h) {
            a.classList.toggle("active", h === current);
        });
    }

    window.addEventListener("scroll", update, { passive: true });
    update();
});