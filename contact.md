---
layout: page
title: Contact
permalink: /contact/
---
<!-- {% raw %}{% seo %}{% endraw %}
 -->

<head>
  <style>
    .contact-page {
      max-width: 720px;
      margin: 40px auto;
      padding: 24px 24px 28px;
      background: #ffffff;
      border-radius: 16px;
      box-shadow:
        0 12px 30px rgba(15, 23, 42, 0.18),
        0 0 0 1px rgba(148, 163, 184, 0.25);
      box-sizing: border-box;
    }

    .contact-heading {
      margin-top: 0;
      margin-bottom: 4px;
      font-size: 1.6rem;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: 0.02em;
    }

    .contact-subtitle {
      margin-top: 0;
      margin-bottom: 24px;
      font-size: 0.98rem;
      color: #4b5563;
      line-height: 1.5;
    }

    .contact-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px 20px;
    }

    .contact-field {
      display: flex;
      flex-direction: column;
    }

    .contact-field-full {
      grid-column: 1 / -1;
    }

    .contact-label {
      font-size: 0.85rem;
      font-weight: 600;
      color: #374151;
      margin-bottom: 6px;
    }

    .contact-input,
    .contact-textarea {
      display: block;
      width: 100%;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid #d1d5db;
      font-size: 0.95rem;
      color: #111827;
      background: #f9fafb;
      box-sizing: border-box;
      transition:
        border-color 150ms ease,
        box-shadow 150ms ease,
        background-color 150ms ease,
        transform 120ms ease;
    }

    .contact-input:focus,
    .contact-textarea:focus {
      outline: none;
      border-color: #16a34a;
      box-shadow:
        0 0 0 1px rgba(22, 163, 74, 0.8),
        0 10px 18px rgba(22, 163, 74, 0.18);
      background: #ffffff;
      transform: translateY(-1px);
    }

    .contact-textarea {
      min-height: 140px;
      resize: vertical;
      line-height: 1.5;
    }

    .contact-helper {
      margin-top: 6px;
      font-size: 0.8rem;
      color: #6b7280;
    }

    .contact-actions {
      margin-top: 24px;
      display: flex;
      justify-content: flex-end;
    }

    .contact-button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 140px;
      padding: 10px 18px;
      border-radius: 9999px;
      border: none;
      background: linear-gradient(135deg, #16a34a, #22c55e);
      color: #ffffff;
      font-weight: 700;
      font-size: 0.95rem;
      letter-spacing: 0.03em;
      text-transform: uppercase;
      cursor: pointer;
      box-shadow:
        0 10px 20px rgba(22, 163, 74, 0.4),
        0 0 0 1px rgba(21, 128, 61, 0.7);
      transition:
        transform 120ms ease,
        box-shadow 120ms ease,
        filter 120ms ease;
    }

    .contact-button:hover {
      transform: translateY(-1px);
      box-shadow:
        0 14px 26px rgba(22, 163, 74, 0.45),
        0 0 0 1px rgba(21, 128, 61, 0.85);
      filter: brightness(1.03);
    }

    .contact-button:active {
      transform: translateY(0);
      box-shadow:
        0 6px 16px rgba(22, 163, 74, 0.45),
        0 0 0 1px rgba(21, 128, 61, 0.9);
      filter: brightness(0.98);
    }

    @media (max-width: 768px) {
      .contact-page {
        margin: 24px auto;
        padding: 20px 18px 24px;
        border-radius: 14px;
      }

      .contact-heading {
        font-size: 1.4rem;
      }

      .contact-grid {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 480px) {
      .contact-page {
        margin: 16px auto;
        padding: 18px 14px 22px;
        box-shadow:
          0 8px 20px rgba(15, 23, 42, 0.18),
          0 0 0 1px rgba(148, 163, 184, 0.2);
      }

      .contact-heading {
        font-size: 1.25rem;
      }

      .contact-subtitle {
        font-size: 0.9rem;
      }
    }
  </style>
</head>

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TTC6RSBSSV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-TTC6RSBSSV');
</script>

<div class="contact-page">
  <h1 class="contact-heading">Get in touch</h1>
  <p class="contact-subtitle">
    Have a question, idea, or opportunity you would like to discuss? Fill out the form below and your message will be delivered directly to my inbox.
  </p>

  <form accept-charset="UTF-8" action="https://getform.io/f/6306f063-5eba-4c08-b8f7-9f2001abdc51" method="POST" enctype="multipart/form-data" target="_blank">
    <div class="contact-grid">
      <div class="contact-field">
        <label for="contact-name" class="contact-label">Name</label>
        <input
          id="contact-name"
          name="name"
          type="text"
          class="contact-input"
          placeholder="Your full name"
          required
        />
      </div>

      <div class="contact-field">
        <label for="contact-email" class="contact-label">Email</label>
        <input
          id="contact-email"
          name="email"
          type="email"
          class="contact-input"
          placeholder="you@example.com"
          required
        />
      </div>

      <div class="contact-field contact-field-full">
        <label for="contact-subject" class="contact-label">Subject</label>
        <input
          id="contact-subject"
          name="subject"
          type="text"
          class="contact-input"
          placeholder="How can I help you?"
          required
        />
      </div>

      <div class="contact-field contact-field-full">
        <label for="contact-message" class="contact-label">Message</label>
        <textarea
          id="contact-message"
          name="message"
          class="contact-textarea"
          placeholder="Write your message here..."
          required
        ></textarea>
        <p class="contact-helper">
          I usually respond within a couple of days.
        </p>
      </div>
    </div>

    <div class="contact-actions">
      <button type="submit" class="contact-button">
        Send message
      </button>
    </div>
  </form>
</div>
