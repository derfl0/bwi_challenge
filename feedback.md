# Feedback

Einige der in der BWI Challenge eingereichten Lösungen besitzen eine „SnakeOil“-Komponente, d.h. sie gaukeln vor, das Problem lösen zu können, obwohl der Lösungsweg speziell an die in der Challenge angegeben Daten angepasst ist. Das ist problematisch, da dann die schnellste Lösung ein einfaches println(„74660“) wäre.

Die „SnakeOil“-Komponente in der Lösung des Gewinners der Challenge ( https://github.com/Molodos/CodingChallenge ) befindet sich in Zeile 69 der ProblemSolver.java. Die optimizeTrucksLoad-Methode erhält eine Magic Number (nennen wir sie N, in diesem Fall 5), um damit die Menge der Lösungen im Lösungsbaum zu begrenzen und schnell eine Lösung zu finden.
Es bleibt die Frage: 

*Woher kommt diese Zahl N?*

Lösung: Es ist die erste Zahl, welche das richtige Ergebnis liefert. Reduzieren wir N auf 4, spuckt der Algorithmus bei gleicher Aufgabenstellung folgendes - leider falsches - Ergebnis aus:

`Summe aller Nutzwerte: 74657`

Die Funktion des Algorithmus tauscht bis zu N Dinge aus, um eine Lösung zu erhalten. Vielleicht löst dieses N=5 ja das Knapsack-Problem und wir können es für immer von unserer NP Liste streichen.

Leider lässt sich relativ schnell ein Gegenbeispiel finden:

**trucks.csv**
```
Name,Kapazität,Gewicht Fahrer
Transporter 1,10000.0,0.0
Transporter 2,10000.0,0.0
```

**items.csv:**

```
Name,Einheiten,Gewicht,Nutzwert
Object A,1000,1001.0,1002.0
Object B,1000,1000.0,1000.0
```

Wir haben also eine Situation mit einem Object A, von dem jeweils 9 Stück in einen Transporter passen und dabei ein bisschen mehr als einen Punkt pro Gramm bringt. Relativ leicht lässt sich erkennen, dass 10x Object B hier die bessere Wahl ist.

Leider kann der Algorithmus des Gewinners dies nicht berechnen, da er dazu in der Lage sein müsste 10 Objekte auszutauschen. Ändert man N auf 10, so kann der Algorithmus wieder das richtige Ergebnis finden.
Also: Problem Solved? Sei N=10? Leider nicht. Lässt man das ursprüngliche Problem mit N=10 laufen, so reicht zumindest der Speicher meiner lokalen Maschine nicht mehr aus:

```
Transporter werden befüllt...fertig
Beladung wird optimiert...Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
        at java.base/java.util.ArrayList.grow(ArrayList.java:239)
        at java.base/java.util.ArrayList.addAll(ArrayList.java:678)
        at com.molodos.codingchallenge.models.ItemTuple.copy(ItemTuple.java:26)
        at com.molodos.codingchallenge.models.ItemList.upgradeTuples(ItemList.java:221)
        at com.molodos.codingchallenge.models.ItemList.getAllTuples(ItemList.java:200)
        at com.molodos.codingchallenge.ProblemSolver.maximizeFreeSpace(ProblemSolver.java:184)
        at com.molodos.codingchallenge.ProblemSolver.optimizeTrucksLoad(ProblemSolver.java:137)
        at com.molodos.codingchallenge.ProblemSolver.solve(ProblemSolver.java:69)
        at com.molodos.codingchallenge.ProblemSolver.main(ProblemSolver.java:42)
 ```

## Fazit

Die zum Sieger gekürte Lösung ist ein etwas umfangreicheres println(„74660“). Das ist sehr schade für alle, die sich mehr mit der Lösung des Problems als mit einer GUI beschäftigt haben.
