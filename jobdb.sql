CREATE DATABASE IF NOT EXISTS job_portal;
USE job_portal;


CREATE TABLE user_information (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_type ENUM('job_seeker', 'employer', 'admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE job_seeker (
    seeker_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    experience INT,
    skills TEXT,
    resume_path VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES user_information(user_id) ON DELETE CASCADE
);

CREATE TABLE employer (
    employer_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    company_name VARCHAR(100) NOT NULL,
    company_website VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES user_information(user_id) ON DELETE CASCADE
);

CREATE TABLE job (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    salary_range VARCHAR(50),
    description TEXT NOT NULL,
    requirements TEXT,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employer_id) REFERENCES employer(employer_id) ON DELETE CASCADE
);

CREATE TABLE application (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    seeker_id INT NOT NULL,
    cover_letter TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'reviewing', 'accepted', 'rejected') DEFAULT 'pending',
    FOREIGN KEY (job_id) REFERENCES job(job_id) ON DELETE CASCADE,
    FOREIGN KEY (seeker_id) REFERENCES job_seeker(seeker_id) ON DELETE CASCADE
);


INSERT INTO user_information (first_name, middle_name, last_name, email, password, user_type) VALUES
('Vinuthna', NULL, 'V', 'vinuthna@example.com', '$2b$12$zJbwK8FzjHFpZcRXJPKlTO9rDZl5XjZ.V5CkGyUIJKMGr.x1mRhMS', 'job_seeker'),
('Sanjeevni', NULL, 'Kumari', 'sanjeevni@example.com', '$2b$12$zJbwK8FzjHFpZcRXJPKlTO9rDZl5XjZ.V5CkGyUIJKMGr.x1mRhMS', 'job_seeker'),
('Cherishka', NULL, 'P', 'cherishka@example.com', '$2b$12$zJbwK8FzjHFpZcRXJPKlTO9rDZl5XjZ.V5CkGyUIJKMGr.x1mRhMS', 'employer'),
('Kasyapa', NULL, 'Sharma', 'kasyapa@example.com', '$2b$12$zJbwK8FzjHFpZcRXJPKlTO9rDZl5XjZ.V5CkGyUIJKMGr.x1mRhMS', 'employer'),
('Aryan', 'Raj', 'Sinha', 'aryan@example.com', '$2b$12$zJbwK8FzjHFpZcRXJPKlTO9rDZl5XjZ.V5CkGyUIJKMGr.x1mRhMS', 'admin');

INSERT INTO job_seeker (user_id, experience, skills, resume_path) VALUES
(1, 5, 'Python, JavaScript, React, SQL', '/resumes/vinuthna_v_resume.pdf'),
(2, 3, 'Java, Spring Boot, MySQL, Agile', '/resumes/sanjeevni_kumari_resume.pdf');

INSERT INTO employer (user_id, company_name, company_website) VALUES
(3, 'Cherishka Corp', 'https://cherishkacorp.com'),
(4, 'Kasyapa Systems', 'https://kasyapasystems.com');

INSERT INTO job (employer_id, title, location, salary_range, description, requirements) VALUES
(1, 'Full Stack Developer', 'New York, NY', '$80,000 - $110,000', 'We are looking for a skilled Full Stack Developer to join our growing team.', 'Experience with React and Python. 3+ years of experience.'),
(1, 'UI/UX Designer', 'Remote', '$70,000 - $90,000', 'Design intuitive user interfaces for our web applications.', 'Portfolio showcasing UI/UX projects. Experience with Figma.'),
(2, 'Data Scientist', 'San Francisco, CA', '$100,000 - $130,000', 'Analyze large datasets to extract insights and build predictive models.', 'Masters in Statistics or Computer Science. Experience with Python and machine learning libraries.'),
(2, 'Project Manager', 'Chicago, IL', '$90,000 - $120,000', 'Lead software development projects from inception to completion.', 'PMP certification. 5+ years of experience managing software projects.');

INSERT INTO application (job_id, seeker_id, cover_letter, status) VALUES
(1, 1, 'I am excited to apply for this position as I have 5 years of experience with the required technologies.', 'reviewing'),
(3, 1, 'My background in data analysis makes me a great fit for this role.', 'pending'),
(2, 2, 'I have always been passionate about creating intuitive user interfaces.', 'pending'),
(4, 2, 'I believe my experience in agile environments would be valuable in this role.', 'accepted');
