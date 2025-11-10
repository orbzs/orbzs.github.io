# Week 5 Assignment
## Task 2: Create database and table in your MySQL server
- Create a new database named website.
- Create a new table named member, in the website database
  > ```sql
  > mysql> create database website;
  > mysql> use website;
  > mysql> create table member (
  > -> id int unsigned primary key auto_increment,
  > -> name varchar(255) not null,
  > -> email varchar(255) not null,
  > -> password varchar(255) not null,
  > -> follower_count int unsigned not null default 0,
  > -> time datetime not null default current_timestamp);
  > ```
  > <img width="961" height="266" alt="image" src="https://github.com/user-attachments/assets/f80a0e03-fc19-44e7-826e-347fc3fdbc7a" /> 

## Task 3: SQL CRUD
- INSERT a new row to the member table where name, email and password must be
set to test, test@test.com, and test. INSERT additional 4 rows with arbitrary data
- SELECT all rows from the member table.
  > ```sql
  > mysql> insert into member(name, email, password)
  >     -> values('test', 'test@test.com', 'test');
  > mysql> insert into member(name, email, password,follower_count)
  >     -> values('2rgv', 'fwafV@daf.com', 'test2', '1');
  > mysql> update member set name='no2'where id=2;
  > mysql> insert into member(name, email, password,follower_count)
  >     -> values('3wef', 'ewfa@ewagv.com', 'fewwfe', '2');
  > mysql> insert into member(name, email, password,follower_count)
  >     -> values('4.iy,', 'o.y.oy@agewv.com', 'yj6', '3');
  > mysql> insert into member(name, email, password,follower_count)
  >     -> values('5fgh', 'naeigr@agew.com', 'abpem', '4');
  > mysql> select * from member;
  > ```
  > <img width="961" height="607" alt="image" src="https://github.com/user-attachments/assets/dbffbcab-4980-488e-8c0c-e6d0abb6cadd" /> 

- SELECT all rows from the member table, in descending order of time.
  > ```sql
  > mysql> select * from member order by time desc;
  > ```
  > <img width="844" height="244" alt="image" src="https://github.com/user-attachments/assets/ff62f2b8-0376-453b-b7b8-263f29bdf80e" /> 

- SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.
  > ```sql
  > mysql> select * from member order by time desc limit 3 offset 1;
  > ```
  > <img width="844" height="192" alt="image" src="https://github.com/user-attachments/assets/3887b32d-cb69-4b44-adf8-53884fa2526a" /> 

- SELECT rows where email equals to test@test.com.
  > ```sql
  > mysql> select * from member where email='test@test.com';
  > ```
  > <img width="844" height="159" alt="image" src="https://github.com/user-attachments/assets/62db09e0-c30b-4cd5-bc89-8dcb8f9f956f" /> 

- SELECT rows where name includes the es keyword.
  > ```sql
  > mysql> select * from member where name like '%es%';
  > ```
  > <img width="844" height="159" alt="image" src="https://github.com/user-attachments/assets/0448cca6-90e7-4654-a259-4e3f4c1c19af" /> 

- SELECT rows where email equals to test@test.com and password equals to test.
  > ```sql
  > mysql> select * from member where email='test@test.com' and password='test';
  > ```
  > <img width="844" height="159" alt="image" src="https://github.com/user-attachments/assets/90807a69-7833-4429-b847-4b7b947a86f5" /> 
- UPDATE data in name column to test2 where email equals to test@test.com.
  > ```sql
  > mysql> update member set name='test2' where email='test@test.com';
  > ``` 
  > <img width="844" height="92" alt="image" src="https://github.com/user-attachments/assets/425ef813-4c7c-4d03-b496-9971e34cbfa9" /> 

## Task 4: SQL Aggregation Functions
- SELECT how many rows from the member table.
  > ```sql
  > mysql> select count(*) from member;
  > ```
  > <img width="844" height="142" alt="image" src="https://github.com/user-attachments/assets/2f814160-5458-4552-99f9-f15ae81b80d1" /> 

- SELECT the sum of follower_count of all the rows from the member table.
  > ```sql
  > mysql> select sum(follower_count) from member;
  > ```
  > <img width="844" height="154" alt="image" src="https://github.com/user-attachments/assets/6b19634b-3218-446f-b653-1fbd46e95d13" />

- SELECT the average of follower_count of all the rows from the member table.
  > ```sql
  > mysql> select avg(follower_count) from member;
  > ```
  > <img width="844" height="147" alt="image" src="https://github.com/user-attachments/assets/ff3427d7-086f-4ee7-8257-685b54a55d48" /> 

- SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
  > ```sql
  > mysql> select avg(follower_count)
  >     -> from(
  >     -> select follower_count
  >     -> from member
  >     -> order by follower_count desc
  >     -> limit 2)
  >     -> as firstfollow2;
  > ```
  > <img width="844" height="261" alt="image" src="https://github.com/user-attachments/assets/d5e80167-1da7-4ea0-a152-08ea2073111e" /> 

## Task 5: SQL JOIN
- Create a new table named message, in the website database.
  > ```sql
  > create table message (
  >     id int unsigned primary key auto_increment,
  >     member_id int unsigned not null,
  >     content text not null,
  >     like_count int unsigned not null default 0,
  >     time datetime not null default current_timestamp,
  >     foreign key (member_id) references member(id));
  > mysql> insert into message(member_id, content, like_count)
  >     -> values(1, 'yetdnwryhrt', 6);
  > mysql> insert into message(member_id, content, like_count)
  >     -> values(2, 'wertfyubbeathb', 41);
  > mysql> insert into message(member_id, content, like_count)
  >     -> values(3, 'tw4hbwnwty', 5);
  > mysql> insert into message(member_id, content, like_count)
  >     -> values(4, 'fjawiofjwafnv', 0);
  > mysql> insert into message(member_id, content, like_count)
  >     -> values(5, 'twhsnwne', 11);
  > ```
  > <img width="844" height="552" alt="image" src="https://github.com/user-attachments/assets/fd0072fb-807c-4237-9ef8-8d1e98dc70e0" />

- SELECT all messages, including sender names. We have to JOIN the member table to get that.
  > ```sql
  > mysql> select message.*, member.name from message
  > -> inner join member on message.member_id=member.id;
  > ```
  > <img width="844" height="234" alt="image" src="https://github.com/user-attachments/assets/f3f43d74-8cc1-4019-ae28-0c6125c019fb" />

- SELECT all messages, including sender names, where sender email equals to test@test.com. We have to JOIN the member table to filter and get that.
  > ```sql
  > mysql> select message.*, member.name
  >     -> from message
  >     -> inner join member on message.member_id=member.id
  >     -> where member.email='test@test.com';
  > ```
  > <img width="844" height="202" alt="image" src="https://github.com/user-attachments/assets/843d625c-da87-485e-8dad-5305553738c7" />

- Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender email equals to test@test.com.
  > ```sql
  > mysql> select avg(message.like_count)
  >     -> from message
  >     -> inner join member on message.member_id = member.id
  >     -> where member.email = 'test@test.com';
  > ```
  > <img width="844" height="214" alt="image" src="https://github.com/user-attachments/assets/fe638e6a-0bb5-4bd6-acc4-84038d7dbed5" />

- Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender email.
  > ```sql
  > mysql> select avg(message.like_count), member.email
  >     -> from message
  >     -> join member on message.member_id=member.id
  >     -> group by email;
  > ```
  > <img width="844" height="284" alt="image" src="https://github.com/user-attachments/assets/4d60ebf1-1ed7-421a-87fd-cd91c9bcd434" />








