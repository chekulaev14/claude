const nodemailer = require('nodemailer');

exports.handler = async (event, context) => {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

  try {
    // Parse request body
    const data = JSON.parse(event.body);
    const { phone, fromCity, toCity, departureDate, formType } = data;

    // Validate required fields
    if (!phone) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Телефон обязателен' })
      };
    }

    // Create transporter using Yandex SMTP
    const transporter = nodemailer.createTransport({
      host: 'smtp.yandex.ru',
      port: 465,
      secure: true,
      auth: {
        user: process.env.YANDEX_EMAIL,
        pass: process.env.YANDEX_APP_PASSWORD
      }
    });

    // Prepare email content based on form type
    let emailSubject = 'Новая заявка с сайта dinamika-cargo.ru';
    let emailText = `Новая заявка:\n\nТелефон: ${phone}\n`;
    let emailHtml = `
      <h2>Новая заявка с сайта</h2>
      <p><strong>Телефон:</strong> ${phone}</p>
    `;

    // Add additional fields if present
    if (fromCity) {
      emailText += `Откуда: ${fromCity}\n`;
      emailHtml += `<p><strong>Откуда:</strong> ${fromCity}</p>`;
    }
    if (toCity) {
      emailText += `Куда: ${toCity}\n`;
      emailHtml += `<p><strong>Куда:</strong> ${toCity}</p>`;
    }
    if (departureDate) {
      emailText += `Дата отправки: ${departureDate}\n`;
      emailHtml += `<p><strong>Дата отправки:</strong> ${departureDate}</p>`;
    }
    if (formType) {
      emailText += `Тип формы: ${formType}\n`;
      emailHtml += `<p><strong>Тип формы:</strong> ${formType}</p>`;
    }

    // Add timestamp
    const timestamp = new Date().toLocaleString('ru-RU', { timeZone: 'Europe/Moscow' });
    emailText += `\nВремя: ${timestamp}`;
    emailHtml += `<p><em>Время: ${timestamp}</em></p>`;

    // Send email
    const info = await transporter.sendMail({
      from: `"ТК Динамика - Заявки" <${process.env.YANDEX_EMAIL}>`,
      to: process.env.RECIPIENT_EMAIL,
      subject: emailSubject,
      text: emailText,
      html: emailHtml
    });

    console.log('Email sent:', info.messageId);

    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        message: 'Заявка успешно отправлена'
      })
    };

  } catch (error) {
    console.error('Error sending email:', error);

    return {
      statusCode: 500,
      body: JSON.stringify({
        error: 'Ошибка при отправке заявки',
        details: error.message
      })
    };
  }
};
