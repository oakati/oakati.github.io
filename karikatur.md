---
layout: page
title: Favorite Caricatures
permalink: /karikatur/
---

<div class="gallery-container">
  {% for item in site.data.karikaturler %}
    <div class="karikatur-item">
      <img src="{{ item.url }}" alt="{{ item.title }}">
    </div>
  {% endfor %}
</div>