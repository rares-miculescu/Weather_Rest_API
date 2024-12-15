# README Tema 2 SCD Rares Dumitru Miculescu 324C3

Tema consista in implementarea unui api care stocheaza date despre vreme global. El foloseste docker compose, care are 3 imagini:

    - API Flask pentru interpretarea cererilor
    - Baza de date pentru stocarea datelor (mongo)
    - Utilitar prin care se pot vedea datele din baza

In cod exista destule comentarii incat sa se poata intelege ce se intampla pe acolo.
Am o observatie de facut. Tema vrea ca un oras sa nu aiba doua temperaturi inregistrate in aceeasi zi. Am implementat acest lucru si imi pica testele de `GET`, pentru ca nu am destule date probabil. Comentand acea portiune, totul ruleaza impecabil, asa ca am hotarat sa las acel cod comentat acolo, pentru a arata la prezentare exact problema.
