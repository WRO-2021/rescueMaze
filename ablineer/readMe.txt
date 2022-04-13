aspettandosi dal lidar un array con le distanze nelle varie direzioni è possibile allineare il robot ai muri senza toccarli,
gira per un tot(ha salvata la velocità di rotazione e il numero di passi/sample del lidar) poi comincia a anallizzare
i dati del lidar finchè non capisce che ha vicino un muro parallelo/perpendicolare:
prima di iniziare cerca un muro affianco a se, o qualche cella più in là se non ce ne sono, ma così perde precisione
poi verso la fine del giro legge a ripetizione i dati del lidar e controllando(ad esempio il muro è subito a fanco) le distanze
a 45° e 135°(se si aspetta che il muro alla fine del giro dovrà essere a destra), finchè non sono uguali(o simili
con uno scarto calcolato in base alla precisione del rilevamento delle distanze e la distanza del muro)

|__/|
|_o_| disegnino del robot che controlla le distanze dagli angoli del muro vicino, se sono uguali allora è allineato
|__\| 

non penso di aver spiegato bene, il codice è più o meno commentato