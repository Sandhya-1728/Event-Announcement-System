const Event = require('../models/Event');
const User = require('../models/User');
const { sendEventReminder } = require('./emailService');

const checkAndSendReminders = async () => {
    try {
        const now = new Date();

        // Find events that need reminders
        const events = await Event.find({
            reminderSent: false,
            date: {
                $gt: now // Only future events
            }
        }).populate('creator');

        for (const event of events) {
            const eventTime = new Date(event.date);
            const reminderTime = new Date(eventTime.getTime() - (event.reminderTime * 60000)); // Convert minutes to milliseconds

            // If it's time to send the reminder
            if (now >= reminderTime) {
                const success = await sendEventReminder(event, event.creator);

                if (success) {
                    // Mark reminder as sent
                    event.reminderSent = true;
                    await event.save();
                }
            }
        }
    } catch (error) {
        console.error('Error in reminder scheduler:', error);
    }
};

// Run the check every minute
const startScheduler = () => {
    setInterval(checkAndSendReminders, 60000); // Check every minute
};

module.exports = {
    startScheduler
}; 