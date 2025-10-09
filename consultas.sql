SELECT yearPublished, COUNT(cod)
FROM documents
WHERE yearpublished <= 2024
GROUP BY yearPublished
ORDER BY yearPublished

SELECT yearpublished,
ROUND(AVG(LENGTH(titleqn))) as mediatamanhotitulo,
MAX(LENGTH(titleqn)) as tamanhomaximo,
MIN(LENGTH(titleqn)) as tamanhominimo
FROM documents
WHERE yearpublished <= 2024
GROUP BY yearpublished
ORDER BY yearpublished

SELECT stddev(medias.mediatamanhotitulo) as desviopadrao
FROM
(SELECT AVG(LENGTH(titleqn)) as mediatamanhotitulo 
FROM documents
WHERE yearpublished <= 2024
GROUP BY yearpublished) as medias

SELECT MAX(LENGTH(titleqn)) as tamanhoMaximo,
MIN(LENGTH(titleqn)) as tamanhoMinimo
FROM documents
WHERE yearpublished <= 2024

SELECT c.yearpublished,
ROUND(AVG(c.qtddpalavratitulo)) as mediatamanhotitulo,
MAX(c.qtddpalavratitulo) as tamanhomaximo,
MIN(c.qtddpalavratitulo) as tamanhominimo
FROM 
(SELECT p.yearpublished, COUNT(p.cod) as qtddpalavratitulo
FROM 
(SELECT yearpublished, cod, regexp_split_to_table(titleqn, '[\s]+') AS palavra
FROM documents WHERE yearpublished <= 2024) p 
GROUP BY p.cod, p.yearpublished) as c
GROUP BY c.yearpublished
ORDER by c.yearpublished

SELECT MAX(c.qtddpalavratitulo) as tamanhomaximo,
MIN(c.qtddpalavratitulo) as tamanhominimo
FROM
(SELECT COUNT(p.cod) as qtddpalavratitulo
FROM 
(SELECT yearpublished, cod, regexp_split_to_table(titleqn, '[\s]+') AS palavra
FROM documents WHERE yearpublished <= 2024) p 
GROUP BY p.cod) as c

SELECT stddev(d.mediatamanhotitulo) as desviopadrao
FROM
(SELECT c.yearpublished, AVG(c.qtddpalavratitulo) as mediatamanhotitulo FROM 
(SELECT p.yearpublished, COUNT(p.cod) as qtddpalavratitulo FROM (SELECT yearpublished, cod, regexp_split_to_table(titleqn, '[\s]+') AS palavra FROM documents WHERE yearpublished <= 2024) p 
GROUP BY p.cod, p.yearpublished) as c
GROUP BY c.yearpublished
) as d

SELECT * FROM
(SELECT yearpublished, SUM((LENGTH(titleqn) - LENGTH(REPLACE(titleqn, ':', '')))) as qtddDoisPontos
FROM documents GROUP BY yearpublished)
NATURAL JOIN
(SELECT yearpublished, SUM((LENGTH(titleqn) - LENGTH(REPLACE(titleqn, ',', '')))) as qtddvirgula
FROM documents GROUP BY yearpublished)
NATURAL JOIN
(SELECT yearpublished, SUM((LENGTH(titleqn) - LENGTH(REPLACE(titleqn, '!', '')))) as qtddexclamacao
FROM documents GROUP BY yearpublished)
NATURAL JOIN
(SELECT yearpublished, SUM((LENGTH(titleqn) - LENGTH(REPLACE(titleqn, '?', '')))) as qtddinterrogacao
FROM documents GROUP BY yearpublished) 
NATURAL JOIN
(SELECT yearpublished, SUM((LENGTH(titleqn) - LENGTH(REPLACE(titleqn, '"', '')))) as qtddaspas
FROM documents GROUP BY yearpublished)
WHERE yearpublished <= 2024
ORDER BY yearpublished

SELECT e.palavra, COUNT(e.palavra) AS qtddPalavras FROM
(SELECT cod, regexp_split_to_table(cleantitleqn, '\s+') AS palavra
FROM documents WHERE language='pt' AND yearpublished <= 2024) e
WHERE e.palavra ~ 'ção$'
GROUP BY e.palavra
ORDER BY  qtddPalavras DESC
LIMIT 10

SELECT e.palavra, COUNT(e.palavra) AS qtddPalavras FROM
(SELECT cod, regexp_split_to_table(cleantitleqn, '\s+') AS palavra
FROM documents WHERE language='pt' AND yearpublished <= 2024) e
WHERE NOT(e.palavra ~ 'ção$')
GROUP BY e.palavra
ORDER BY  qtddPalavras DESC
LIMIT 10

SELECT e.yearPublished, COUNT(e.cod) qtddpalavrascao FROM
(SELECT cod, yearPublished, TRIM(regexp_split_to_table(cleantitleqn, '\s+')) AS palavra
FROM documents WHERE language='pt' AND yearpublished <= 2024) e
WHERE e.palavra ~ 'ção$'
GROUP BY e.yearPublished
ORDER BY e.yearPublished

SELECT e.yearPublished, COUNT(e.cod) qtddpalavrasnaocao FROM
(SELECT cod, yearPublished, regexp_split_to_table(cleantitleqn, '\s+') AS palavra
FROM documents WHERE language='pt' AND yearpublished <= 2024) e
WHERE NOT(e.palavra ~ 'ção$')
GROUP BY e.yearPublished
ORDER BY e.yearPublished

SELECT symbol, COUNT(z) as qtdd 
FROM
(SELECT c.symbol, k.yearpublished, c.z , k.palavra
FROM chemicalelements AS c, (SELECT yearpublished, TRIM(regexp_split_to_table(titleqn, '[\s]+')) AS palavra
FROM documents WHERE yearpublished <= 2024) k
WHERE k.palavra LIKE unaccent(c.symbol) OR k.palavra ILIKE unaccent(c.name) 
OR k.palavra ILIKE unaccent(c.latim) OR k.palavra ILIKE unaccent(c.englishname)
OR k.palavra ILIKE unaccent(c.spanishname))
GROUP BY symbol
ORDER BY qtdd DESC
LIMIT 11

SELECT symbol, yearpublished, COUNT(z) as qtdd
FROM
(SELECT c.symbol, k.yearpublished, c.z , k.palavra
FROM chemicalelements AS c, (SELECT yearpublished, TRIM(regexp_split_to_table(titleqn, '[\s]+')) AS palavra
FROM documents WHERE yearpublished <= 2024) k
WHERE k.palavra LIKE unaccent(c.symbol) OR k.palavra ILIKE unaccent(c.name)
OR k.palavra ILIKE unaccent(c.latim) OR k.palavra ILIKE unaccent(c.englishname)
OR k.palavra ILIKE unaccent(c.spanishname))
GROUP BY symbol, yearpublished
ORDER BY yearpublished

SELECT CORR(tamanhoTitulo, citations) 
FROM
(SELECT LENGTH(titleqn) as tamanhoTitulo, citations
FROM documents WHERE yearpublished <= 2024)
	
SELECT yearPublished, ROUND(AVG(citations)) AS mediacitacoes
FROM documents
WHERE yearpublished <= 2024
GROUP BY yearPublished
HAVING
AVG(citations) IS NOT NULL
ORDER BY yearPublished

SELECT
CORR(LENGTH(titleqn), CASE WHEN type='article' THEN 1 ELSE 0 END) corrtituloartigo,
CORR(LENGTH(titleqn), CASE WHEN type='review' THEN 1 ELSE 0 END) corrtituloreview
FROM documents

SELECT yearPublished, COUNT(cod) as qtddartigos
FROM documents 
WHERE type = 'article' AND yearpublished <= 2024
GROUP BY yearPublished
ORDER BY yearPublished

SELECT yearPublished, COUNT(cod) as qtddrevisoes
FROM documents 
WHERE type = 'review' AND yearpublished <= 2024
GROUP BY yearPublished
ORDER BY yearPublished

SELECT CORR(tamanhoTitulo, quantidadeAutores) 
FROM
(SELECT LENGTH(d.titleqn) as tamanhoTitulo, COUNT(d.cod) as quantidadeAutores FROM documents d 
INNER JOIN authors a ON d.cod = a.cod
WHERE d.yearpublished <= 2024 
GROUP BY d.cod)

SELECT p.yearPublished, ROUND(AVG(p.quantidadeAutores)) AS mediaquantidadeautores FROM (
SELECT yearPublished, LENGTH(d.titleqn) AS tamanhoTitulo, COUNT(d.cod) AS quantidadeAutores FROM documents d
INNER JOIN authors a ON d.cod = a.cod WHERE d.yearpublished <= 2024 
GROUP BY d.cod) p
GROUP BY p.yearPublished
ORDER BY p.yearPublished

SELECT yearpublished, COUNT(cod) as qtdddocumentos
FROM documents WHERE language='en' AND yearpublished <= 2024
GROUP BY yearpublished
ORDER BY yearpublished

SELECT pr.prefix, COUNT(p.cod) as qtdd
FROM 
(SELECT cod, regexp_split_to_table(cleantitleqn, '[\s]+') AS palavra
FROM documents WHERE language='pt' AND yearpublished <= 2024) p
INNER JOIN prefixes pr 
ON p.palavra ~ CONCAT('^', pr.prefix)
GROUP BY pr.prefix
ORDER BY qtdd DESC
LIMIT 10

SELECT p.yearPublished, COUNT(p.palavra) as qtddprefixos
FROM 
(SELECT yearPublished, TRIM(regexp_split_to_table(cleantitleqn, '[\s]+')) AS palavra
FROM documents WHERE language='pt' AND yearpublished <= 2024) p
INNER JOIN prefixes pr 
ON p.palavra ~ CONCAT('^', pr.prefix)
GROUP BY p.yearPublished
ORDER BY  p.yearPublished

SELECT COUNT(p.palavra) as qtdd, p.palavra , '', '' FROM 
(SELECT yearPublished, LOWER(regexp_split_to_table(cleantitleqn, '[\s]+')) AS palavra FROM documents) p
WHERE p.yearpublished > 2019 AND p.yearPublished <= 2024
GROUP BY p.palavra
ORDER BY qtdd DESC

SELECT COUNT(p.palavra) as qtdd, p.palavra , '', '' FROM 
(SELECT yearPublished, LOWER(regexp_split_to_table(cleantitleqn, '[\s]+')) AS palavra FROM documents) p
WHERE p.yearpublished < 1983
GROUP BY p.palavra
ORDER BY qtdd DESC

SELECT AVG(LENGTH(frases.frase)) 
FROM
(SELECT TRIM(regexp_split_to_table(RTRIM(abstract, '.'), '[\.]+')) AS frase
FROM documents WHERE yearPublished <= 2024) AS frases

SELECT p.yearPublished, ROUND(AVG(LENGTH(p.frase))) as mediaNumeroFrasesAbstract FROM
(SELECT yearPublished, TRIM(regexp_split_to_table(RTRIM(abstract, '.'), '[\.]+')) AS frase
FROM documents WHERE yearPublished <= 2024) p
GROUP BY p.yearPublished
ORDER BY yearPublished

SELECT r.yearPublished, ROUND(AVG(r.qtddpalavrasfrase)) as medianumeropalavrasporfrase FROM (
SELECT q.yearPublished, q.frase, COUNT(cod) as qtddpalavrasfrase FROM
(SELECT p.cod, p.yearPublished, p.frase, regexp_split_to_table(frase, '[\s]+') AS palavra FROM
(SELECT cod, yearPublished, TRIM(regexp_split_to_table(RTRIM(abstract, '.'), '[\.]+')) AS frase
FROM documents WHERE yearPublished <= 2024) p) q
GROUP BY q.frase, q.yearPublished) r
GROUP BY r.yearPublished

SELECT AVG(LENGTH(abstract)) FROM documents WHERE yearPublished <= 2024

SELECT yearPublished, ROUND(AVG(LENGTH(abstract))) AS mediaTamanhoAbstract FROM documents
WHERE yearPublished <= 2024
GROUP BY yearPublished
HAVING
AVG(LENGTH(abstract)) IS NOT NULL
ORDER BY yearPublished

SELECT yearpublished, titleqn, frase, symbol FROM
(SELECT k.yearpublished, k.titleqn, k,frase, c.symbol
FROM chemicalelements AS c, 
(
SELECT e.titleqn, e.frase, e.yearpublished, TRIM(regexp_split_to_table(e.frase, '[\s]+')) AS palavra
FROM 
(
SELECT titleqn, yearpublished, TRIM(regexp_split_to_table(titleqn, '(: )|(- )|(\. )')) AS frase
FROM documents
) e
) k
WHERE k.palavra LIKE unaccent(c.symbol)) d
WHERE d.frase ~ ('^' || d.symbol || ' ')
