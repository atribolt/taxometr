create table task (
    id integer primary key,
    title varchar(255) unique not null
);

create table label (
    id bigint primary key,
    "name" varchar(255) unique not null
);

create table timings (
    id bigint primary key,
    task_id integer not null,
    start timestamp not null,
    finish timestamp default null,

    foreign key (task_id) references task(id) 
        on delete cascade
        on update cascade
);

create table task_label_link (
    task_id integer not null,
    label_id bigint not null,

    primary key (task_id, label_id),
    foreign key (task_id) references task(id),
    foreign key (label_id) references label(id)
);


insert into task (id, title) values 
    (1, 'task 1'),
    (2, 'task 2'),
    (3, 'task 3')
;

insert into label (id, "name") values 
    (1, 'label task 1'),
    (2, 'label task 2'),
    (3, 'label task 3'),
    (4, 'label task 1 2'),
    (5, 'label task 2 3')
;

