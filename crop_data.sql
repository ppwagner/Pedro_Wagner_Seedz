CREATE TABLE crop_data (
	cod_nivel_territorial int2,
	nivel_territorial varchar,
	cod_unidade_medida int2,
	unidade_medida varchar,
	valor varchar,
	cod_municipio int4,
	cod_ano int4,
	ano int4,
	cod_produto_lavouras_temporarias int4,
	produto_lavouras_temporarias varchar,
	cod_variavel int4,
	variavel varchar
);

INSERT INTO crop_data (cod_nivel_territorial,nivel_territorial,cod_unidade_medida,unidade_medida,valor,cod_municipio,cod_ano,ano,cod_produto_lavouras_temporarias,produto_lavouras_temporarias,cod_variavel,variavel) VALUES
	 (6,'Município',1,'Hectares',111,444,2011,2011,555,'Soja (em grão)',666,'Área plantada'),
