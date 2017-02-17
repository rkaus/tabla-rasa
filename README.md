# tabla-rasa

innovative ai that applies natural language markov modelling techniques to written [tabla](https://en.wikipedia.org/wiki/Tabla) (percussion) music compositions.

###  how to read the sample output:
- refer to the wiki link above
- [7min video](https://www.youtube.com/watch?v=CG0yl7X8L7s) explanation of tabla basics
- [further reading](http://chandrakantha.com/tablasite/bsicbols.htm)


### sample output from this model:
- NA GE NA TII; NA GE NA TII;
- KA NA TA KA; NA RE RE KAT; KA NA TA KA; NA RE RE KAT;
- TA KA TAA -; KI TA TA KA; TAA - TIN NA; KI TA TA KA; TA KA TAA -; KI TA TA KA; TAA - TIN NA; KI TA TA KA;
- GE TI RA KI; TA GHI - NA; GE TI RA KI; TA TAA KI NA;GE TI RA KI; TA GHI - NA; GE TI RA KI; TA TAA KI NA;


###  important files:
- scrape.py : collects and formats composition data
- run.py : generates and outputs tabla compositions
- markov_model : creates a dictionary containing n-gram counts


### lessons learned:
- 
