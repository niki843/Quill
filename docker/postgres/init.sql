-- Create BlogPosts table 
CREATE TABLE blog_posts (
    blog_post_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    published_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create BlogComment table 
CREATE TABLE blog_comment ( 
    comment_id SERIAL PRIMARY KEY,
    blog_post_id INTEGER NOT NULL,
    comment TEXT NOT NULL,
    commented_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_blog_comment_blog_post FOREIGN KEY (blog_post_id) REFERENCES blog_posts(blog_post_id)
);

-- Insert BlogPosts data 
INSERT INTO blog_posts (blog_post_id, title, body, published_on)
VALUES (1, 'How to bake a cake', 'Blog body', '2020-02-01'),
(2, 'How to bake cookies', 'Blog body', '2020-02-14'),
(3, 'How to bake bread', 'Blog body', '2020-02-25'),
(4, 'How to make custard', 'Blog body', '2020-03-10'),
(5, 'The joys of raisins', 'Blog body', '2020-03-16'),
(6, 'Making pizza dough', 'Blog body', '2020-03-28'),
(7, 'To kneed, or not to kneed, that is the question', 'Blog body', '2020-04-04'),
(8, 'Is Bake Off better on Channel 4?', 'Blog body', '2020-04-21'),
(9, 'The perfect Victoria Sponge', 'tes', '2020-03-01'),
(10, 'How to make acroissant', 'test', '2020-02-01');

-- Reset sequence to continue from highest ID 
SELECT setval('blog_posts_blog_post_id_seq', (SELECT MAX(blog_post_id) FROM blog_posts));

-- Insert BlogComment data 
INSERT INTO blog_comment (comment_id, blog_post_id, comment, commented_on) 
VALUES (1, 2, 'These are great cookies.', '2020-02-14 18:42:44.158'),
(2, 6, 'Fairly average dough.', '2020-04-08 11:56:21.136'),
(3, 2, 'Yummy cookies.', '2020-03-08 10:25:35.215'),
(4, 4, 'My custard was lumpy.', '2020-04-08 08:56:12.109'),
(5, 7, 'Comment body', '2020-05-10 11:21:08.112'),
(6, 1, 'Comment body', '2020-02-21 11:46:18.147');

-- -- Reset sequence to continue from highest ID 
SELECT setval('blog_comment_comment_id_seq', (SELECT MAX(comment_id) FROM blog_comment));