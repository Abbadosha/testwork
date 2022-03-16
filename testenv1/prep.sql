create table if not exists user_tbl(
user_id SERIAL PRIMARY KEY,
email text,
password text);

CREATE TABLE public.article_tbl (
	article_id serial4 NOT NULL,
	user_id int4 NULL,
	article_name text NULL,
	article text NULL,
	CONSTRAINT article_tbl_pkey PRIMARY KEY (article_id),
	CONSTRAINT article_tbl_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user_tbl(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE public.video_tbl (
	video_id serial4 NOT NULL,
	user_id int4 NULL,
	video_name text NULL,
	video_url text NULL,
	CONSTRAINT video_tbl_pkey PRIMARY KEY (video_id),
	CONSTRAINT video_tbl_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user_tbl(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);
	

CREATE TABLE public."comments" (
	comment_id serial4 NOT NULL,
	user_id int4 NULL,
	comments_txt text NULL,
	video_id int4 NULL,
	article_id int4 NULL,
	CONSTRAINT comments_pkey PRIMARY KEY (comment_id),
	CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user_tbl(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fk_article_id FOREIGN KEY (article_id) REFERENCES public.article_tbl(article_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fk_video_id FOREIGN KEY (video_id) REFERENCES public.video_tbl(video_id) ON DELETE CASCADE ON UPDATE CASCADE
);



