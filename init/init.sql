create table member(
id int(4) zerofill not null,
romaji varchar(25) not null,
name varchar(15) not null,
furigana varchar(20) not null,
-- affiliation varchar(15) not null,
introduction varchar(50) not null,
follows int(8) not null default 0,
subscribes int(8) not null default 0,
primary key(id)
);

-- UPDATE member SET id = 0000 WHERE id = 0100;
-- alter table member drop column affiliation;

-- alter table member modify column follows int(8) not null default 0;
-- alter table member modify column subscribes int(8) not null default 0;


create table feed(
id int(7) zerofill not null,
post datetime not null,
mid int(4) zerofill not null,
link varchar(200) not null,
title varchar(500) not null,
snippet varchar(80) not null,
thumbnail tinyint(1) not null,
favors int(8) not null default 0,
primary key(id),
index(post,mid),
foreign key(mid) references member(id) on delete cascade on update cascade
);


-- alter table feed modify column favors int(8) not null default 0;

-- alter table feed change image thumbnail tinyint(1) not null


-- create table photo(
-- mid int(4) not null,
-- fid int(7) not null,	
-- mark int(4) not null,
-- type varchar(4) not null,
-- post datetime not null,
-- url varchar(400) not null,
-- width int(4) not null,
-- height int(4) not null,
-- status tinyint(1) not null,
-- primary key(mid,fid,mark),
-- foreign key(mid) references member(id) on delete cascade on update cascade,
-- foreign key(fid) references feed(id) on delete cascade
-- );


create table photo(
fid int(7) zerofill not null,
sequence int(4) zerofill not null,
type varchar(4) not null,
url varchar(400) not null,
width int(4) not null,
height int(4) not null,
status tinyint(1) not null,
primary key(fid,sequence),
foreign key(fid) references feed(id) on delete cascade
);


create table blog(
id int(7) zerofill not null,
text_original mediumtext,
title_translated varchar(500) not null,
text_translated mediumtext,
html_reserve mediumtext,
primary key(id),
foreign key(id) references feed(id) on delete cascade
);


create table user(
id int(8) zerofill not null auto_increment,
last_active datetime not null,
ip_address varchar(15) not null,
user_agent varchar(400) not null,
end_point varchar(240) not null,
primary key(id)
);

-- alter table user modify column last_active datetime not null;


create table follow(
uid int(8) zerofill not null,
mid int(4) zerofill not null,
primary key(uid,mid),
foreign key(uid) references user(id) on delete cascade,
foreign key(mid) references member(id) on delete cascade on update cascade
);


create table subscription(
uid int(8) zerofill not null,
mid int(4) zerofill not null,
primary key(uid,mid),
foreign key(uid) references user(id) on delete cascade,
foreign key(mid) references member(id) on delete cascade on update cascade
);


create table favor(
uid int(8) zerofill not null,
fid int(7) zerofill not null,
primary key(uid,fid),
foreign key(uid) references user(id) on delete cascade,
foreign key(fid) references feed(id) on delete cascade
);


create table push(
pid varchar(19) not null,
fid int(7) zerofill not null,
push datetime not null,
primary key(pid,fid),
foreign key(fid) references feed(id) on delete cascade
);

-- alter table push modify column push datetime not null;


-- trigger
delimiter $

create trigger favors_autoincrease
after insert on favor
for each row
begin
	update feed set favors = (select count(*) from favor where favor.fid = new.fid) where feed.id = new.fid;
end;
$
create trigger favors_autodecrease
after delete on favor
for each row
begin
	update feed set favors = (select count(*) from favor where favor.fid = old.fid) where feed.id = old.fid;
end;
$



create trigger follows_autoincrease
after insert on follow
for each row
begin
	update member set follows = (select count(*) from follow where follow.mid = new.mid) where member.id = new.mid;
end;
$
create trigger follows_autodecrease
after delete on follow
for each row
begin
	update member set follows = (select count(*) from follow where follow.mid = old.mid) where member.id = old.mid;
end;
$



create trigger subscribes_autoincrease
after insert on subscription
for each row
begin
	update member set subscribes = (select count(*) from subscription where subscription.mid = new.mid) where member.id = new.mid;
end;
$
create trigger subscribes_autodecrease
after delete on subscription
for each row
begin
	update member set subscribes = (select count(*) from subscription where subscription.mid = old.mid) where member.id = old.mid;
end;
$

delimiter ;