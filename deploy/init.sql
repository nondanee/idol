create database idol;

use idol;

create table raw(
id int(6) not null,
team tinyint(1) not null,
author varchar(15) not null,
post datetime not null,
link varchar(200) not null,
title varchar(500) not null,
article mediumtext,
capture datetime not null,
PRIMARY KEY(id,team)
);



create table list(
id int(6) not null,
team tinyint(1) not null,
post datetime not null,
kana varchar(20) not null,
rome varchar(25) not null,
author varchar(15) not null,
link varchar(200) not null,
title varchar(500) not null,
brief varchar(100) not null,
PRIMARY KEY(id,team),
INDEX(post,kana)
);


create table photo(
rome varchar(25) not null,
filename varchar(50) not null,
author varchar(15) not null,
url varchar(400) not null,
status tinyint(1) default 0,
PRIMARY KEY(rome,filename)
);


create table blog(
id int(6) not null,
team tinyint(1) not null,
post datetime not null,
rome varchar(25) not null,
author varchar(15) not null,
link varchar(200) not null,
title_original varchar(500) not null,
title_translation varchar(500) not null,
text_original mediumtext,
text_translation mediumtext,
PRIMARY KEY(id,team),
INDEX(post,rome)
);