---
layout: default
title: Home
---

<p class="home-description">{{ site.description }}</p>

<div class="section-grid">
{% for section in site.doc_sections %}
{% assign items = site.docs | where: "section", section.id | sort: "order" %}
{% if items.size > 0 %}
<section class="section-card">
    <h2>{{ section.title }}</h2>
    <ul>
    {% for d in items %}
        <li>
            <a href="{{ d.url | relative_url }}">{{ d.title }}</a>
            {% if d.description %}<span class="muted">{{ d.description }}</span>{% endif %}
        </li>
    {% endfor %}
    </ul>
</section>
{% endif %}
{% endfor %}
</div>