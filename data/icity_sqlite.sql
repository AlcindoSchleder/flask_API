PRAGMA foreign_keys = ON;

CREATE TABLE languages (
	pk_languages integer primary key autoincrement,
	dsc_lang varchar(50) NOT NULL,
	symb_lang varchar(5) NOT NULL,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	date_update timestamp
);

DROP TABLE countries;

CREATE TABLE countries(
	pk_countries smallint NOT NULL,
	fk_languages smallint NOT NULL,
	dsc_country varchar(50) NOT NULL,
	sym_country varchar(5) NOT NULL,
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	CONSTRAINT pk_countries PRIMARY KEY (pk_countries),
	FOREIGN KEY(fk_languages) REFERENCES languages(pk_languages)
		on update restrict
		on delete restrict
);

CREATE TABLE states(
	fk_countries smallint NOT NULL,
	pk_states character(2) NOT NULL,
	dsc_state varchar(80) NOT NULL,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	date_update timestamp,
	CONSTRAINT pk_states PRIMARY KEY (fk_countries,pk_states),
	FOREIGN KEY (fk_countries) REFERENCES countries(pk_countries)
	    on delete cascade
	    on update cascade
);

CREATE TABLE cities(
	fk_countries smallint NOT NULL,
	fk_states character(2) NOT NULL,
	pk_cities integer NOT NULL,
	flag_cap smallint NOT NULL DEFAULT 0,
	dsc_cities varchar(80) NOT NULL,
	zip_code varchar(15),
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	CONSTRAINT pk_cities PRIMARY KEY (fk_countries,fk_states,pk_cities),
	FOREIGN KEY (fk_countries, fk_states) 
	REFERENCES states(fk_countries, pk_states)
	    on delete cascade
	    on update cascade
);

CREATE INDEX ak_zip_code ON cities (fk_countries, fk_states, zip_code);

CREATE TABLE registers(
	pk_registers integer PRIMARY KEY autoincrement,
	type_owner smallint NOT NULL DEFAULT 0 check(type_owner in (0, 1)),
	user_name varchar(50) NOT NULL,
	alias_reg varchar(50),
	user_login varchar(50) NOT NULL,
	user_pwd varchar(255),
	reg_score smallint NOT NULL DEFAULT 0,
	flag_confirmed smallint NOT NULL DEFAULT 0 check(flag_confirmed in (0, 1)),
	flag_mailer smallint NOT NULL DEFAULT 1 check(flag_mailer in (0, 1)),
	expire_date timestamp,
	hash_data varchar(64) NOT NULL,
	blockchain_account varchar(128),
	update_date timestamp,
	insert_date timestamp NOT NULL DEFAULT current_timestam
);

CREATE TABLE type_contacts(
	pk_type_contacts integer primary key autoincrement,
	dsc_tcnt varchar(50) NOT NULL,
	flag_tcnt smallint NOT NULL DEFAULT 0 check(flag_tcnt >= 0 and flag_tcnt <= 6),
	mask_contact varchar(128),
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp
);

CREATE TABLE partners(
	fk_registers integer NOT NULL,
	vlr_vda numeric(11,2) DEFAULT 0.00,
	dsc_tab numeric(4,2) DEFAULT 0.00,
	cms_partner numeric(4,2) DEFAULT 0.00,
	flag_resseler smallint NOT NULL DEFAULT 0,
	qtd_days_pgto_cms smallint,
	val_cms numeric(11,2) DEFAULT 0.00,
	insert_date timestamp NOT NULL DEFAULT current_timestamp,
	update_date timestamp,
	CONSTRAINT pk_partners PRIMARY KEY (fk_registers),
	FOREIGN KEY (fk_registers) 
	REFERENCES registers(pk_registers)
	    on delete cascade
	    on update cascade
);

CREATE TABLE enterprise(
	pk_enterprise smallint NOT NULL,
	fk_countries smallint NOT NULL,
	fk_states character(2) NOT NULL,
	fk_cities integer NOT NULL,
	cnpj_comp varchar(20) NOT NULL,
	ie_comp varchar(30) NOT NULL,
	dsc_comp varchar(50) NOT NULL,
	address_comp varchar(50) NOT NULL,
	num_comp integer NOT NULL,
	quarter_comp varchar(50),
	compl_comp varchar(50),
	zip_comp varchar(15) NOT NULL,
	image_comp blob,
	qtd_connected smallint,
	qtd_access smallint NOT NULL,
	flag_published smallint NOT NULL DEFAULT 0,
	views_comp integer,
	image_type character varying(255),
	image_size integer,
	title_comp character varying(255),
	about_comp text,
	web_address character varying(255),
	points_comp integer,
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	CONSTRAINT pk_enterprise PRIMARY KEY (pk_enterprise)

);

CREATE TABLE type_documents(
	pk_type_documents integer primary key autoincrement,
	dsc_tdoc varchar(50) NOT NULL,
	obs_tdoc text,
	qtd_item smallint NOT NULL,
	flag_tdoc smallint NOT NULL DEFAULT 0 check(flag_tdoc >= 0 and flag_tdoc <= 21),
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp
);

CREATE TABLE enterprise_documents(
	pk_enterprise_documents integer primary key autoincrement,
	fk_enterprise smallint NOT NULL,
	fk_type_documents smallint NOT NULL,
	document blob not null,
	hasd_doc varchar(64),
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	FOREIGN KEY (fk_enterprise) 
	REFERENCES enterprise(pk_enterprise)
	    on delete cascade
	    on update cascade,
	FOREIGN KEY (fk_type_documents) 
	REFERENCES type_documents(pk_type_documents)
	    on delete cascade
	    on update cascade
);

CREATE TABLE registers_enterprise(
	fk_enterprise smallint NOT NULL,
	fk_registers integer NOT NULL,
	flag_default smallint NOT NULL DEFAULT 0,
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	CONSTRAINT pk_registers_company PRIMARY KEY (fk_enterprise,fk_registers),
	FOREIGN KEY (fk_enterprise) 
	REFERENCES enterprise(pk_enterprise)
	    on delete cascade
	    on update cascade,
	FOREIGN KEY (fk_registers) 
	REFERENCES registers(pk_registers)
	    on delete cascade
	    on update cascade
);

CREATE TABLE registers_contacts(
	fk_registers integer NOT NULL,
	pk_registers_contacts smallint NOT NULL,
	fk_type_contacts integer NOT NULL,
	name_contact varchar(50) NOT NULL,
	cnt_reg_cnt varchar(255) NOT NULL,
	dta_evt date,
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	CONSTRAINT pk_registers_contacts PRIMARY KEY (fk_registers,pk_registers_contacts),
	FOREIGN KEY (fk_registers) 
	REFERENCES registers(pk_registers)
	    on delete cascade
	    on update cascade
);

CREATE TABLE public.registers_observation(
	fk_registers integer NOT NULL,
	obs_cstm text NOT NULL,
	insert_date timestamp NOT NULL DEFAULT current_timestamp,
	update_date timestamp,
	CONSTRAINT pk_registers_observation PRIMARY KEY (fk_registers),
	FOREIGN KEY (fk_registers) 
	REFERENCES registers(pk_registers)
	    on delete cascade
	    on update cascade
);

CREATE TABLE registers_sessions(
	pk_registers_sessions varchar(64) NOT NULL,
	fk_registers integer NOT NULL,
	session_name varchar(255) NOT NULL,
	expires timestamp NOT NULL,
	last_access timestamp NOT NULL DEFAULT current_timestamp,
	elapsed_time timestamp,
	qtd_access smallint NOT NULL,
	qtd_connected smallint NOT NULL,
	qtd_access_comp smallint NOT NULL,
	qtd_connected_comp smallint NOT NULL,
	client_ip varchar(15) NOT NULL,
	host_name varchar(50) NOT NULL,
	session_agent varchar(255) NOT NULL,
	request_uri text NOT NULL,
	expire_date timestamp,
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	CONSTRAINT pk_registers_sessions PRIMARY KEY (pk_registers_sessions),
	FOREIGN KEY (fk_registers) 
	REFERENCES registers(pk_registers)
	    on delete cascade
	    on update cascade
);

CREATE TABLE sessions_views(
	fk_registers_sessions varchar(64) NOT NULL,
	pk_sessions_views integer NOT NULL,
	online_startview timestamp NOT NULL,
	online_endview timestamp NOT NULL,
	online_ip varchar(15) NOT NULL,
	fk_domains varchar(255) NOT NULL,
	online_uri text NOT NULL,
	online_agent varchar(255) NOT NULL,
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	CONSTRAINT pk_sessions_views PRIMARY KEY (fk_registers_sessions,pk_sessions_views)
);

CREATE TABLE suppliers(
	fk_registers integer NOT NULL,
	last_buy date,
	last_buy_value numeric(11,2) DEFAULT 0.00,
	last_call_date timestamp,
	sld_supp numeric(11,2) DEFAULT 0.00,
	insert_date timestamp NOT NULL DEFAULT current_timestamp,
	update_date timestamp,
	CONSTRAINT pk_suppliers PRIMARY KEY (fk_registers),
	FOREIGN KEY (fk_registers) 
	REFERENCES registers(pk_registers)
	    on delete cascade
	    on update cascade
);

CREATE TABLE customers(
	fk_registers integer NOT NULL,
	flag_share_balanace smallint NOT NULL DEFAULT 0,
	flag_cnsm smallint NOT NULL DEFAULT 0,
	flag_block smallint NOT NULL DEFAULT 0,
	balance numeric(11,2) NOT NULL DEFAULT 0.00,
	credit_limit numeric(11,4) NOT NULL DEFAULT 0.0000,
	date_block date,
	motv_block character varying(128),
	insert_date timestamp NOT NULL DEFAULT current_timestamp,
	update_date timestamp,
	CONSTRAINT pk_customers PRIMARY KEY (fk_registers),
	FOREIGN KEY (fk_registers) 
	REFERENCES registers(pk_registers)
	    on delete cascade
	    on update cascade
);

CREATE TABLE categories(
	pk_categories integer primary key autoincrement,
	dsc_tcat varchar(50) NOT NULL,
	flag_tcat smallint NOT NULL DEFAULT 0 check(flag_tcar >=0 and flag_tcat <= 5),
	flag_default smallint NOT NULL DEFAULT 0 check(flag_default in (0, 1)),
	date_update timestamp,
	date_insert public.timestamp_default NOT NULL DEFAULT current_timestamp
);

CREATE TABLE registers_categories(
	fk_registers integer NOT NULL,
	fk_categories smallint NOT NULL,
	flag_active smallint not null default 0 check(flag_active in (0, 1)),
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	CONSTRAINT pk_registers_categories PRIMARY KEY (fk_registers,fk_categories),
	FOREIGN KEY (fk_registers) 
	REFERENCES registers(pk_registers)
	    on delete cascade
	    on update cascade,
	FOREIGN KEY (fk_categories) 
	REFERENCES categories(pk_categories)
	    on delete cascade
	    on update cascade
);

CREATE TABLE type_addresses(
	pk_type_addresses integer primary key autoincrement,
	dsc_addr varchar(50) NOT NULL,
	flag_taddr smallint NOT NULL default 0 check(flag_taddr in (0, 1, 2, 3, 4)),
	update_date timestamp,
	insert_date timestamp NOT NULL DEFAULT current_timestamp
);

CREATE table registers_addresses(
	fk_registers integer NOT NULL,
	fk_type_addresses integer NOT NULL,
	fk_countries smallint NOT NULL,
	fk_states character(2) NOT NULL,
	fk_cities integer NOT NULL,
	address varchar(50),
	number smallint,
	quarter varchar(50),
	zip_code varchar(15),
	complement varchar(50),
	insert_date timestamp NOT NULL DEFAULT current_timestamp,
	update_date timestamp,
	CONSTRAINT pk_registers_addresses PRIMARY KEY (fk_registers,fk_type_addresses),
	FOREIGN KEY (fk_registers) 
	REFERENCES registers(pk_registers)
	    on delete cascade
	    on update cascade,
	FOREIGN KEY (fk_countries, fk_states, fk_cities) 
	REFERENCES cities(fk_countries, fk_states, pk_cities)
	    on delete cascade
	    on update cascade
);

CREATE TABLE registers_documents(
	fk_registers integer NOT NULL,
	pk_registers_documents varchar(64) NOT NULL,
	fk_type_documents smallint NOT NULL,
	update_doc timestamp,
	document blob not null,
	flag_docid smallint NOT NULL DEFAULT 0,
	update_date timestamp,
	insert_date timestamp not null default current_timestamp,
	CONSTRAINT pk_registers_documents PRIMARY KEY (fk_registers,pk_registers_documents,fk_type_documents),
	FOREIGN KEY (fk_registers) 
	REFERENCES registers(pk_registers)
	    on delete cascade
	    on update cascade,
	FOREIGN KEY (fk_type_documents) 
	REFERENCES type_documents(pk_type_documents)
	    on delete cascade
	    on update cascade
);

CREATE TABLE registers_images(
	fk_registers integer NOT NULL,
	pk_registers_images varchar(64) NOT NULL,
	reg_image blob NOT NULL,
	flag_default smallint NOT NULL DEFAULT 1 check(flag_default in (0, 1)),
	date_update timestamp,
	date_insert timestamp NOT NULL DEFAULT current_timestamp,
	CONSTRAINT pk_registers_imags PRIMARY KEY (fk_registers,pk_registers_images),
	FOREIGN KEY (fk_registers) 
	REFERENCES registers(pk_registers)
	    on delete cascade
	    on update cascade
);
