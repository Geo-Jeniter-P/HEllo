document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    AOS.init();

    const contactForm = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');

    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();

            formMessage.textContent = 'Sending your message...';
            formMessage.style.color = '#014244';

            const formData = new FormData(contactForm);

            fetch('/send_email', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(errorData.message || 'Server responded with an error');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    formMessage.textContent = data.message;
                    formMessage.style.color = 'green';
                    contactForm.reset();
                } else {
                    formMessage.textContent = data.message;
                    formMessage.style.color = 'red';
                }
            })
            .catch(error => {
                console.error('Error submitting form:', error);
                formMessage.textContent = `An error occurred: ${error.message || 'Please try again later.'}`;
                formMessage.style.color = 'red';
            });
        });
    }
});