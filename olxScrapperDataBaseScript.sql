-- use scrapperdb;
select * from contactInfo

-- alter table contactInfo add constraint makingUniqueAddId UNIQUE (AddId);
create table OlxData(ContactId int primary Key,Name varchar(255),PhoneNumber varchar(255),MemberSince varchar(255),
AddPosted date,Address date,Addid varchar(255) UNIQUE,Price varchar(255),AddHeading varchar(255), AddCategory varchar(255),
 AddDescription varchar(3000),RecordAdded date);
select * from OlxData

alter table contactInfo add UNIQUE(AddId)




