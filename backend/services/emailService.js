const nodemailer = require('nodemailer');

// Create a transporter using SMTP
const transporter = nodemailer.createTransport({
    service: process.env.EMAIL_SERVICE, // e.g., 'gmail'
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD
    }
});

const sendEventReminder = async (event, user) => {
    const mailOptions = {
        from: process.env.EMAIL_USER,
        to: user.email,
        subject: `Reminder: ${event.title} is starting soon!`,
        html: `
            <h2>Event Reminder</h2>
            <p>Your event "${event.title}" is starting in ${event.reminderTime} minutes!</p>
            <p><strong>Details:</strong></p>
            <ul>
                <li>Date: ${new Date(event.date).toLocaleDateString()}</li>
                <li>Time: ${new Date(event.date).toLocaleTimeString()}</li>
                <li>Location: ${event.location}</li>
            </ul>
            <p>Description: ${event.description}</p>
        `
    };

    try {
        await transporter.sendMail(mailOptions);
        return true;
    } catch (error) {
        console.error('Error sending email:', error);
        return false;
    }
};

module.exports = {
    sendEventReminder
}; 