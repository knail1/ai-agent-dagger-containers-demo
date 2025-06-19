CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    quote TEXT NOT NULL,
    author TEXT NOT NULL
);

INSERT INTO quotes (quote, author) VALUES 
('Life is what happens when you're busy making other plans.', 'John Lennon'),
('Be yourself; everyone else is already taken.', 'Oscar Wilde'),
('Two things are infinite: the universe and human stupidity.', 'Albert Einstein');