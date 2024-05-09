// src/components/EmailForm.tsx
import React, { useState } from 'react';
import axios from 'axios';

interface FormData {
  event_id: string;
  email_subject: string;
  email_content: string;
  timestamp: string;
}

const EmailForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    event_id: '',
    email_subject: '',
    email_content: '',
    timestamp: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/save_emails', formData);
      console.log(response.data);
      // Optionally, you can reset the form after successful submission
      setFormData({
        event_id: '',
        email_subject: '',
        email_content: '',
        timestamp: ''
      });
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>Save Email</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Event ID:</label>
          <input type="text" name="event_id" value={formData.event_id} onChange={handleChange} />
        </div>
        <div>
          <label>Email Subject:</label>
          <input type="text" name="email_subject" value={formData.email_subject} onChange={handleChange} />
        </div>
        <div>
          <label>Email Content:</label>
          <textarea name="email_content" value={formData.email_content} onChange={handleChange} />
        </div>
        <div>
          <label>Timestamp:</label>
          <input type="datetime-local" name="timestamp" value={formData.timestamp} onChange={handleChange} />
        </div>
        <button type="submit">Save Email</button>
      </form>
    </div>
  );
};

export default EmailForm;
