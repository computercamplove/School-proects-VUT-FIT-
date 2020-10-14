--=====================================--
-- Name: IDS Projekt - SQL
-- Authors: Abikenova Zhamilya (xabike00)
--          Glos Kristian      (xglosk00)
--=====================================--
-- FOR SELECT TO SHOW CORRECT TIME DATE
ALTER SESSION SET nls_date_format = "YYYY-MM-DD hh24:MI";
-- / DROP TABLE and SEQ / --
DROP SEQUENCE res_seq;
DROP TABLE users                    CASCADE CONSTRAINTS;
DROP TABLE employee                 CASCADE CONSTRAINTS;
DROP TABLE client                   CASCADE CONSTRAINTS;
DROP TABLE reservation              CASCADE CONSTRAINTS;
DROP TABLE service                  CASCADE CONSTRAINTS;
DROP TABLE service_x_employee       CASCADE CONSTRAINTS;
DROP TABLE reservation_x_service    CASCADE CONSTRAINTS;
DROP TABLE equipmente               CASCADE CONSTRAINTS;
DROP TABLE reservation_x_equipmente CASCADE CONSTRAINTS;
DROP TABLE studio                   CASCADE CONSTRAINTS;
DROP TABLE reservation_x_studio     CASCADE CONSTRAINTS;
DROP TABLE compensation             CASCADE CONSTRAINTS;
DROP TABLE type_equip               CASCADE CONSTRAINTS;



-- / CREATE TABLE / --
CREATE TABLE users (
    id INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
    user_name      VARCHAR(128) NOT NULL,
    birth_number   NUMBER NOT NULL UNIQUE,
    address        VARCHAR(128) NOT NULL,
    phone_number   VARCHAR(128) NOT NULL
);

CREATE TABLE employee (
    user_id        INT NOT NULL PRIMARY KEY,
    position_job   VARCHAR(128) NOT NULL,
    salary         NUMBER NOT NULL
);

CREATE TABLE client (
    user_id        INT NOT NULL PRIMARY KEY,
    company_name   VARCHAR(128),
    bank_account   VARCHAR(128) NOT NULL
);

CREATE TABLE reservation (
    pk_reservation   NUMBER PRIMARY KEY,
    payment_method   VARCHAR(80) NOT NULL,
    note             VARCHAR(128),
    final_price      NUMBER NOT NULL,
    client_id        INT NOT NULL,
    CHECK (final_price >= 0),
    CHECK (payment_method = 'Card' OR payment_method = 'Cash')
);

CREATE SEQUENCE res_seq;


CREATE TABLE service (
    pk_service     INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
    service_type   VARCHAR(128) NOT NULL,
    price          NUMBER(15, 5) NOT NULL,
    CHECK (price >= 0)
);

CREATE TABLE service_x_employee (
    pk_service_employee   INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
    service_id            INT NOT NULL,
    employee_id           INT NOT NULL
);

CREATE TABLE reservation_x_service (
    pk_reservation_service   INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
    reservation_id           INT NOT NULL,
    service_id               INT NOT NULL,
    start_res                DATE NOT NULL,
    end_res                  DATE NOT NULL,
    CHECK (start_res < end_res)
);

CREATE TABLE equipmente (
  PK_equip INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
  name_eq VARCHAR(128) NOT NULL,
  date_of_manufacture DATE NOT NULL, --YYYY-MM-DD
  condition VARCHAR(128),
  price NUMBER NOT NULL,
  description_eq VARCHAR(128),
  type_ID INT NOT NULL,
  CHECK (price >= 0)
);

CREATE TABLE type_equip (
  PK_type INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
  name_type VARCHAR(128) NOT NULL UNIQUE
);

CREATE TABLE reservation_x_equipmente (
    pk_reservation_x_equipmente   INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
    reservation_id                INT NOT NULL,
    equipmente_id                 INT NOT NULL
);

CREATE TABLE studio (
  PK_studio INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
  area NUMBER NOT NULL,
  note VARCHAR(128),
  price NUMBER(15, 5) NOT NULL,
  address VARCHAR(128) NOT NULL,
  CHECK (price >= 0)
);

CREATE TABLE reservation_x_studio (
    pk_reservation_x_studio   INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
    reservation_id            INT NOT NULL,
    studio_id                 INT NOT NULL,
    start_res                 DATE NOT NULL,
    end_res                   DATE NOT NULL,
    CHECK (start_res < end_res)
);

CREATE TABLE compensation (
    pk_compensation   INT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,
    payment           NUMBER NOT NULL,
    id_reservation    INT NOT NULL,
    id_equipmente     INT,
    id_studio         INT,
    CHECK (payment >= 0)
);

-- / ALTER TABLE / -- for foreign keys
-- users
ALTER TABLE employee
    ADD CONSTRAINT employee_user_id_fk FOREIGN KEY ( user_id )
        REFERENCES users ( id )
            ON DELETE CASCADE;

ALTER TABLE client
    ADD CONSTRAINT client_user_id_fk FOREIGN KEY ( user_id )
        REFERENCES users ( id )
            ON DELETE CASCADE;

--rezervation
ALTER TABLE reservation
    ADD CONSTRAINT user_reservation_id_fk FOREIGN KEY ( client_id )
        REFERENCES client (user_id )
            ON DELETE CASCADE;

--service_x_employee
ALTER TABLE service_x_employee
    ADD CONSTRAINT service_x_employee_service_id_fk FOREIGN KEY ( service_id )
        REFERENCES service ( pk_service )
            ON DELETE CASCADE;

ALTER TABLE service_x_employee
    ADD CONSTRAINT service_x_employee_employee_id_fk FOREIGN KEY ( employee_id )
        REFERENCES employee ( user_id )
            ON DELETE CASCADE;

--reservation_x_service
ALTER TABLE reservation_x_service
    ADD CONSTRAINT reservation_x_service_reservation_id_fk FOREIGN KEY ( reservation_id )
        REFERENCES reservation ( pk_reservation )
            ON DELETE CASCADE;

ALTER TABLE reservation_x_service
    ADD CONSTRAINT reservation_x_service_service_id_fk FOREIGN KEY ( service_id )
        REFERENCES service ( pk_service )
            ON DELETE CASCADE;

--reservation_x_equipmente
ALTER TABLE reservation_x_equipmente
    ADD CONSTRAINT reservation_x_equipmente_reservation_id_fk FOREIGN KEY ( reservation_id )
        REFERENCES reservation ( pk_reservation )
            ON DELETE CASCADE;

ALTER TABLE reservation_x_equipmente
    ADD CONSTRAINT reservation_x_equipmente_eq_id_fk FOREIGN KEY ( equipmente_id )
        REFERENCES equipmente ( pk_equip )
            ON DELETE CASCADE;

--reservation_x_studio
ALTER TABLE reservation_x_studio
    ADD CONSTRAINT reservation_x_studio_reservation_id_fk FOREIGN KEY ( reservation_id )
        REFERENCES reservation ( pk_reservation )
            ON DELETE CASCADE;

ALTER TABLE reservation_x_studio
    ADD CONSTRAINT reservation_x_studio_studio_id_fk FOREIGN KEY ( studio_id )
        REFERENCES studio ( pk_studio )
            ON DELETE CASCADE;

--compensation
ALTER TABLE compensation
    ADD CONSTRAINT compensation_equipmente_id_fk FOREIGN KEY ( id_equipmente )
        REFERENCES equipmente ( pk_equip )
            ON DELETE CASCADE;

ALTER TABLE compensation
    ADD CONSTRAINT compensation_studio_id_fk FOREIGN KEY ( id_studio )
        REFERENCES studio ( pk_studio )
            ON DELETE CASCADE;

ALTER TABLE compensation
    ADD CONSTRAINT compensation_reservation_id_fk FOREIGN KEY ( id_reservation )
        REFERENCES reservation ( pk_reservation )
            ON DELETE CASCADE;
            
--equipmente
ALTER TABLE equipmente
    ADD CONSTRAINT equipmente_type_id_fk FOREIGN KEY ( type_id )
        REFERENCES type_equip ( pk_type )
            ON DELETE CASCADE;
            
-- TRIGGER


CREATE OR REPLACE TRIGGER reservation_pk_id BEFORE INSERT ON reservation
FOR EACH ROW
    BEGIN
       SELECT res_seq.nextval 
       INTO :NEW.pk_reservation
       FROM dual;
    END;
/

CREATE OR REPLACE TRIGGER birth_number_of_client BEFORE
    INSERT OR UPDATE OF birth_number ON users
FOR EACH ROW DECLARE
    dd             VARCHAR2(2);
    mm             VARCHAR2(2);
    yy             VARCHAR2(2);
    RCplus         BOOLEAN;
    ECP            BOOLEAN;
    birth_number   users.birth_number%TYPE;
BEGIN
    birth_number := :new.birth_number;
    IF ( length(birth_number) > 10 OR length(birth_number) < 9 ) THEN
        raise_application_error(-20000, 'The birth number is less than 9 characters or longer than 10 characters.');
    END IF;

if ( length(birth_number) = 10 AND MOD(birth_number, 11) != 0 ) THEN
    raise_application_error(-20001, 'The birth number is not divisible by 11.');
END
if;

IF ( length(birth_number) = 9 AND substr(birth_number, 7, 3) = '000' ) THEN
    raise_application_error(-20002, 'Shouldnt be 000');
END IF;
   --YY-MM-DD-KKK(K).

dd := substr(birth_number, 5, 2);

mm := substr(birth_number, 3, 2);

yy := substr(birth_number, 1, 2);
   --YY [0-99]
   
RCplus:=false;
ECP:=false;

IF ( yy < 0 OR yy > 99 ) THEN
    raise_application_error(-20003, 'Wrong birth number format');
END IF;

IF ( mm > 50 ) THEN
    mm := mm - 50;
ELSE
    IF ( mm > 20 ) THEN
        mm := mm - 20;
        RCplus:=true;
    END IF;
END IF;
   --MM [1-12]

IF ( mm <= 0 OR mm > 12 ) THEN
    raise_application_error(-20003, 'Wrong birth number format');
END IF;

IF ( mm = 2 AND mod(yy, 4) = 0
                AND ( dd > 29 ) ) THEN
    raise_application_error(-20003, 'Wrong birth number format');
END IF;

IF ( mm = 2 AND mod(yy, 4) != 0
                AND ( dd > 28 ) ) THEN
    raise_application_error(-20003, 'Wrong birth number format');
END IF;

IF ( ( mm = 1 OR mm = 3
                 OR mm = 5
                    OR mm = 7
                       OR mm = 8
                          OR mm = 10
                             OR mm = 12 ) AND dd > 31 ) THEN
    raise_application_error(-20003, 'Wrong birth number format');
END IF;

IF ( ( mm = 4 OR mm = 6
                 OR mm = 9
                    OR mm = 11 ) AND dd > 30 ) THEN
    raise_application_error(-20003, 'Wrong birth number format');
END IF;

IF ( dd <= 0 ) THEN
    raise_application_error(-20003, 'Wrong birth number format');
END IF;

IF ( dd > 40 ) THEN
    dd := dd - 40;
    ECP := true;
END IF;

IF RCplus AND ECP THEN
    raise_application_error(-20003, 'Wrong birth number format');
END IF;

end;
/  


--PROCEDURES
CREATE OR REPLACE PROCEDURE female_reservations_between (
    studiog     studio.address%TYPE,
    date_from   DATE,
    date_to     DATE
) AS

    CURSOR useri IS
    SELECT DISTINCT
        birth_number,
        user_name,
        studio.address,
        start_res,
        COUNT(user_name) AS number_of_reservations
    FROM
        users,
        reservation,
        reservation_x_studio,
        studio
    WHERE
        users.id = client_id
        AND pk_reservation = reservation_id
        AND studio_id = pk_studio
    GROUP BY
        birth_number,
        user_name,
        studio.address,
        start_res
    ORDER BY
        user_name;

    counting            INTEGER;
    isfemale            INTEGER;
    o                   useri%rowtype;
    reservation_count   INTEGER;
    currentname         users.user_name%TYPE;
BEGIN
    counting := 0;
    reservation_count := 0;
    currentname := 'nil';
    dbms_output.put_line('Female reservations for studio:');
    OPEN useri;
    LOOP
        FETCH useri INTO o; -- line from cursor
        EXIT WHEN useri%notfound; -- end cycle if cursor ends
        isfemale := substr(o.birth_number, 3, 2);
        IF studiog = o.address AND isfemale > 50 AND TO_DATE(o.start_res) BETWEEN date_from AND date_to THEN
            IF currentname != o.user_name AND currentname != 'nil' THEN
                dbms_output.put_line('Name: '
                                     || currentname
                                     || ' || '
                                     || 'birth number: '
                                     || o.birth_number
                                     || ' || '
                                     || ' number of reservations for the studio: '
                                     || reservation_count);

                reservation_count := 1;
            ELSE
                reservation_count := reservation_count + 1;
            END IF;

            currentname := o.user_name;
            counting := counting + 1;
        END IF;

    END LOOP;

    dbms_output.put_line('Name: '
                         || o.user_name
                         || ' || '
                         || 'birth number: '
                         || o.birth_number
                         || ' || '
                         || ' number of reservations for the studio: '
                         || reservation_count);

    dbms_output.put_line('Total: ' || counting);
    CLOSE useri;
EXCEPTION
    WHEN OTHERS THEN
        raise_application_error(-20004, 'error in procedure');
END;
/

CREATE OR REPLACE PROCEDURE control_phone_number AS
    CURSOR users IS
    SELECT
        *
    FROM
        users;

    record users%rowtype;
BEGIN
    OPEN users;
    LOOP
        FETCH users INTO record;
        EXIT WHEN users%notfound;
        IF ( NOT regexp_like(record.phone_number, '^(\+420)?\s?[1-9][0-9]{2}\s?[0-9]{3}\s?[0-9]{3}$') ) THEN
            dbms_output.put_line('User '
                                 || record.user_name
                                 || ' '
                                 || 'has phone number which doesnt work: '
                                 || record.phone_number);
        END IF;

    END LOOP;

    CLOSE users;
EXCEPTION
    WHEN OTHERS THEN
        raise_application_error(-20005, 'Error control_phone_number');
END;
/
   
-- / INSERT INTO / --
INSERT INTO users(user_name,birth_number,address,phone_number)VALUES('Arnold Red',490320554,'Purkynova 59','+42000775617498');
INSERT INTO users(user_name,birth_number,address,phone_number)VALUES('Chris Jamey',7903200019,'Skacelova 16','+420999309300');
INSERT INTO users(user_name,birth_number,address,phone_number)VALUES('Jon Snail',9203200017,'northern alley','+420900400499');
INSERT INTO users(user_name,birth_number,address,phone_number)VALUES('Jozef Novák',9603200013,'Hlavní','+420944450075');
INSERT INTO users(user_name,birth_number,address,phone_number)VALUES('Kristian Sedum',9002270013,'Komin 79','+420900227013');
INSERT INTO users(user_name,birth_number,address,phone_number)VALUES('Jan Novák',8702270016,'Hlavní 0','+420870227016');

--for procedure
INSERT INTO users(user_name,birth_number,address,phone_number)VALUES('Veronika GLos',8753200016,'Komin 23','+420944457675');
INSERT INTO users(user_name,birth_number,address,phone_number)VALUES('Tereza J.',9159270010,'Hlavní 6','+420915927010');
INSERT INTO users(user_name,birth_number,address,phone_number)VALUES('Veronika Hlavní',9853200016,'Hlavní','+420944457455');

INSERT INTO employee VALUES(6,'Fotograf',20000);
INSERT INTO employee VALUES(4,'Cameraman',15000.58);
INSERT INTO employee VALUES(5,'Assistant',22000);

INSERT INTO client VALUES (1,'Oracle',44488); 
INSERT INTO client VALUES (2,'AVAST',2233355588); 
INSERT INTO client VALUES (3,NULL,2233355588); 

INSERT INTO client VALUES (7,NULL,0000000);
INSERT INTO client VALUES (8,NULL,9999999); 
INSERT INTO client VALUES (9,NULL,88888); 

INSERT INTO reservation(payment_method,note,final_price,client_id)VALUES('Cash',NULL,6000,3);
INSERT INTO reservation(payment_method,note,final_price,client_id)VALUES('Card','Variabilny symbol: 44887272' ,48000.15,7);
INSERT INTO reservation(payment_method,note,final_price,client_id)VALUES('Card','dakujem pekne',4600.15,2);
INSERT INTO reservation(payment_method,note,final_price,client_id)VALUES('Card','na patek' ,4815,7);
INSERT INTO reservation(payment_method,note,final_price,client_id)VALUES('Card', NULL,48222215,7);
INSERT INTO reservation(payment_method,note,final_price,client_id)VALUES('Card','na patek' ,48222215,7);
INSERT INTO reservation(payment_method,note,final_price,client_id)VALUES('Card','na patek' ,48,8);
INSERT INTO reservation(payment_method,note,final_price,client_id)VALUES('Card','na patek' ,4812,8);
INSERT INTO reservation(payment_method,note,final_price,client_id)VALUES('Card','na patek' ,4812,9);

INSERT INTO service(service_type,price) VALUES ('Photographing',1500);
INSERT INTO service(service_type,price) VALUES ('Video recording',3000);
INSERT INTO service(service_type,price) VALUES ('Small tasks',1000);

INSERT INTO service_x_employee(service_id,employee_id) VALUES (2,4);
INSERT INTO service_x_employee(service_id,employee_id) VALUES (1,6);
INSERT INTO service_x_employee(service_id,employee_id) VALUES (3,5);

INSERT INTO reservation_x_service (reservation_id, service_id, start_res, end_res) 
VALUES (4, 1,  TO_DATE('2019-03-20 11:10', 'yyyy-mm-dd hh24:mi:ss'), TO_DATE('2019-03-20 15:00', 'yyyy-mm-dd hh24:mi:ss'));

INSERT INTO type_equip (name_type) VALUES ('Computer');
INSERT INTO type_equip (name_type) VALUES ('Notebook');
INSERT INTO type_equip (name_type) VALUES ('Camera');
INSERT INTO type_equip (name_type) VALUES ('Lamp');
INSERT INTO type_equip (name_type) VALUES ('Tripod');

INSERT INTO equipmente (name_eq, date_of_manufacture, condition, price, description_eq, type_ID) 
VALUES ('MacBook Air', TO_DATE('2011-03-15', 'yyyy-mm-dd'), 'Good', 30, 'MacBook Air made in China', 1);
INSERT INTO equipmente (name_eq, date_of_manufacture, condition, price, type_ID) 
VALUES ('Cannon', TO_DATE('2015-04-15', 'yyyy-mm-dd'), 'Okay', 500, 3);
INSERT INTO equipmente (name_eq, date_of_manufacture, condition, price, description_eq, type_ID) 
VALUES ('NIKON 200', TO_DATE('2017-03-15', 'yyyy-mm-dd'), 'Broken lens', 90, 'made in Amerika', 3);
INSERT INTO equipmente (name_eq, date_of_manufacture, price, description_eq, type_ID) 
VALUES ('Lamp for portret', TO_DATE('2009-03-15', 'yyyy-mm-dd'), 100, 'made in Canada', 4);
INSERT INTO equipmente (name_eq, date_of_manufacture, price, type_ID) 
VALUES ('Velikan', TO_DATE('2010-03-15', 'yyyy-mm-dd'), 150, 5);
INSERT INTO equipmente (name_eq, date_of_manufacture, condition, price, description_eq, type_ID) 
VALUES ('MacBook PRO', TO_DATE('2011-03-15', 'yyyy-mm-dd'), 'Good', 600, 'MacBook PRO made in China', 2);

INSERT INTO studio (area, note, price, address) 
VALUES (10, 'In a good qualaty', 1000, 'Skacelova 15');
INSERT INTO studio (area, note, price, address) 
VALUES (20, 'For daytime', 2000, 'Respublika 40');
INSERT INTO studio (area, price, address) 
VALUES (50, 3000, 'Dominikanska 40');
INSERT INTO studio (area, price, address) 
VALUES (60, 5000, 'Komin 40');

INSERT INTO studio (area, price, address) 
VALUES (15, 7000, 'Komin 77');
INSERT INTO studio (area, price, address) 
VALUES (25, 2000, 'Hlavni 90');
INSERT INTO studio (area, price, address) 
VALUES (30, 4000, 'Komin 60');
INSERT INTO studio (area, price, address) 
VALUES (40, 9000, 'Grohova 10');


INSERT INTO reservation_x_equipmente (reservation_id, equipmente_id) VALUES (2,3);
INSERT INTO reservation_x_equipmente (reservation_id, equipmente_id) VALUES (1,2);
INSERT INTO reservation_x_equipmente (reservation_id, equipmente_id) VALUES (3,3);

INSERT INTO reservation_x_studio (reservation_id,studio_id,start_res,end_res)
VALUES(2,4, TO_DATE('2010-03-11 12:00', 'yyyy-mm-dd hh24:mi:ss'), TO_DATE('2010-03-11 16:00', 'yyyy-mm-dd hh24:mi:ss'));
INSERT INTO reservation_x_studio (reservation_id,studio_id,start_res,end_res)
VALUES(3,3, TO_DATE('2019-03-13 10:15', 'yyyy-mm-dd hh24:mi:ss'), TO_DATE('2019-03-13 18:00', 'yyyy-mm-dd hh24:mi:ss'));
INSERT INTO reservation_x_studio (reservation_id,studio_id,start_res,end_res)
VALUES(1,4, TO_DATE('2006-03-01 15:00', 'yyyy-mm-dd hh24:mi:ss'), TO_DATE('2006-03-01 18:30', 'yyyy-mm-dd hh24:mi:ss'));
INSERT INTO reservation_x_studio (reservation_id,studio_id,start_res,end_res)
VALUES(4,4, TO_DATE('2005-03-20 14:00', 'yyyy-mm-dd hh24:mi:ss'), TO_DATE('2005-03-20 15:00', 'yyyy-mm-dd hh24:mi:ss'));


INSERT INTO reservation_x_studio (reservation_id,studio_id,start_res,end_res)
VALUES(5,4, TO_DATE('2008-03-25 14:00', 'yyyy-mm-dd hh24:mi:ss'), TO_DATE('2008-03-25 15:00', 'yyyy-mm-dd hh24:mi:ss'));
INSERT INTO reservation_x_studio (reservation_id,studio_id,start_res,end_res)
VALUES(6,4, TO_DATE('2009-7-25 14:00', 'yyyy-mm-dd hh24:mi:ss'), TO_DATE('2009-7-25 15:00', 'yyyy-mm-dd hh24:mi:ss'));
INSERT INTO reservation_x_studio (reservation_id,studio_id,start_res,end_res)
VALUES(7,4, TO_DATE('2007-03-11 14:00', 'yyyy-mm-dd hh24:mi:ss'), TO_DATE('2007-03-11 15:00', 'yyyy-mm-dd hh24:mi:ss'));
INSERT INTO reservation_x_studio (reservation_id,studio_id,start_res,end_res)
VALUES(8,4, TO_DATE('2009-03-18 14:00', 'yyyy-mm-dd hh24:mi:ss'), TO_DATE('2009-03-18 15:00', 'yyyy-mm-dd hh24:mi:ss'));
INSERT INTO reservation_x_studio (reservation_id,studio_id,start_res,end_res)
VALUES(9,4, TO_DATE('2010-03-18 14:00', 'yyyy-mm-dd hh24:mi:ss'), TO_DATE('2010-03-18 15:00', 'yyyy-mm-dd hh24:mi:ss'));

INSERT INTO compensation (payment, id_reservation, id_equipmente) VALUES (1000, 2, 3);
INSERT INTO compensation (payment, id_reservation, id_studio) VALUES (500, 3, 3);



--[3rd part of project: SELECTS]

-- 1. Show address of studios and their price if they cost less than 3000 (2 tables)
SELECT studio.address, studio.price
FROM reservation_x_studio JOIN studio ON reservation_x_studio.studio_id = studio.pk_studio
WHERE studio.price < 3000;

-- 2. Show service that is currently not reserved (2 tables)
SELECT service.service_type
FROM service JOIN reservation_x_service ON service.pk_service = reservation_x_service.service_id;

--1. Show all clients with pending compensations, and the fee they have to pay (3 tables)
SELECT client.bank_account, compensation.payment, reservation.payment_method
FROM client JOIN reservation ON client.user_id = reservation.client_id
    JOIN compensation ON compensation.id_reservation = reservation.pk_reservation;

--1. Show for every equipment type the number of equipments falling within it, then sort them from max to min
-- (group by + agregace)
SELECT type_equip.name_type,
COUNT (*) AS "Number of equipment" 
FROM type_equip JOIN equipmente ON equipmente.type_id = type_equip.pk_type
GROUP BY type_equip.name_type 
ORDER BY "Number of equipment" DESC;

--2. Show all clients and their total payment for all reserved studios (group by + agregace)
SELECT reservation.client_id, SUM(studio.price) AS "Total price"
FROM studio JOIN reservation_x_studio ON studio.pk_studio = reservation_x_studio.studio_id
JOIN reservation ON reservation_x_studio.reservation_id = reservation.pk_reservation
GROUP BY reservation.client_id;


--1. Show all reserved equipment (exist)           
SELECT equipmente.name_eq
FROM equipmente
WHERE EXISTS (SELECT *
                FROM reservation_x_equipmente 
                WHERE equipmente.pk_equip = reservation_x_equipmente.equipmente_id);

--1. Show all equipment names that fall under the type Camera, and their price (IN)
 SELECT name_eq, price
 FROM equipmente
 WHERE  type_id IN (SELECT pk_type
                        FROM type_equip
                        WHERE type_equip.name_type = 'Camera');
      
      
      
-- EXPLAIN PLAN: 
--1. Show for every equipment type the number of equipments falling within it, then sort them from max to min

EXPLAIN PLAN FOR
SELECT type_equip.name_type,
COUNT (*) AS "Number of equipment" 
FROM type_equip JOIN equipmente ON equipmente.type_id = type_equip.pk_type
GROUP BY type_equip.name_type 
ORDER BY "Number of equipment" DESC;

SELECT plan_table_output FROM table (dbms_xplan.display());

CREATE INDEX index_name_type_x_equipmente ON equipmente(type_ID);

EXPLAIN PLAN FOR
SELECT type_equip.name_type,
COUNT (*) AS "Number of equipment" 
FROM type_equip JOIN equipmente ON equipmente.type_id = type_equip.pk_type
GROUP BY type_equip.name_type 
ORDER BY "Number of equipment" DESC; 

SELECT plan_table_output FROM table (dbms_xplan.display());                        

DROP INDEX index_name_type_x_equipmente;
--[4-5 part of project] -                      
GRANT ALL ON users                    TO XGLOSK00;
GRANT ALL ON employee                 TO XGLOSK00;
GRANT ALL ON client                   TO XGLOSK00;
GRANT ALL ON reservation              TO XGLOSK00;
GRANT ALL ON service                  TO XGLOSK00;
GRANT ALL ON service_x_employee       TO XGLOSK00;
GRANT ALL ON reservation_x_service    TO XGLOSK00;
GRANT ALL ON equipmente               TO XGLOSK00;
GRANT ALL ON reservation_x_equipmente TO XGLOSK00;
GRANT ALL ON studio                   TO XGLOSK00;
GRANT ALL ON reservation_x_studio     TO XGLOSK00;
GRANT ALL ON compensation             TO XGLOSK00;
GRANT ALL ON type_equip               TO XGLOSK00;

GRANT EXECUTE ON female_reservations_Between TO XGLOSK00;
GRANT EXECUTE ON control_phone_number        TO XGLOSK00;

DROP MATERIALIZED VIEW equipments_type_and_price;

CREATE materialized view equipments_type_and_price cache -- optimalize reading from view
    build immediate -- view immediately filled upon building
    refresh
        ON commit
as -- refreshes on commit
  -- show equipment's type and price
  SELECT XABIKE00.equipmente.name_eq, XABIKE00.equipmente.price, XABIKE00.type_equip.name_type
  FROM XABIKE00.equipmente JOIN XABIKE00.type_equip ON XABIKE00.equipmente.type_ID = XABIKE00.type_equip.pk_type
  ORDER BY XABIKE00.equipmente.name_eq;

GRANT ALL ON equipments_type_and_price TO xglosk00;


--DEMONSTARTION HOW WORKS 4-5 PART OF PROJECT

--DEMOSTRATION OF MATERIALIZED VIEW
select * from equipments_type_and_price;
INSERT INTO type_equip (name_type) VALUES ('Wall for Photographing');
INSERT INTO equipmente (name_eq, date_of_manufacture, condition, price, description_eq, type_ID) 
VALUES ('Wally', TO_DATE('2011-03-15', 'yyyy-mm-dd'), 'Good', 30, 'made in China', 6);
select * from equipments_type_and_price;--unchanged material view
COMMIT; -- COMMIT actualize view
select * from equipments_type_and_price;--actualized view

--DEMONSTRATION FOR SECOND MEMBER
--select * from equipments_type_and_price;
--INSERT INTO XABIKE00.type_equip (name_type) VALUES ('Wall for Photographing');
--INSERT INTO XABIKE00.equipmente (name_eq, date_of_manufacture, condition, price, description_eq, type_ID) 
--VALUES ('Wally', TO_DATE('2011-03-15', 'yyyy-mm-dd'), 'Good', 30, 'made in China', 6);
--select * from equipments_type_and_price;--unchanged material view
--COMMIT; -- COMMIT actualize view
--select * from equipments_type_and_price;--actualized view


--Check if trigger is working
SELECT pk_reservation FROM reservation;

--Check trigger to control birth number
--INSERT INTO users(user_name,birth_number,address,phone_number)VALUES('A Red',49032000554,'Purkynova 59','+420975617498');

--Control procedure female_reservations_between
--finds all reservetions for women in dates from and to, based on studio, and counts the number of them
--DBMS OUTPUT
/*Female reservations for studio:
  Name: Tereza J. || birth number: 8753200016 ||  number of reservations for the studio: 2
  Name: Veronika GLos || birth number: 9853200016 ||  number of reservations for the studio: 4
  Name: Veronika Hlavní || birth number: 9853200016 ||  number of reservations for the studio: 1
  Celkem: 7*/
BEGIN
  female_reservations_Between('Komin 40',TO_DATE('2005-01-01', 'yyyy-mm-dd'),TO_DATE('2010-12-31', 'yyyy-mm-dd'));
END;
/
--Procedure to check validity of phone number of all registered users
--DBMS OUTPUT
--User Arnold Red has phone number which doesnt work: +42000775617498
begin 
control_phone_number;
end;
/
