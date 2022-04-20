package pacco;

import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.DeliverCallback;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicReference;

/**
 * main con rabbitmq, legge dalla coda Esplorazione, i mezzaggi devono cominciare con
 * "Esplora:" , poi in base alla lettera dopo fa diverse cose:
 * w set wall
 * m do movements
 * f flags
 * u track to unknown cell
 * controllare il codice per maggiori specifiche
 * ci sono due argomenti da linea di comando:
 * -h help
 * -v verbose
 *
 * @author Samuele Facenda
 * @mail samule.facenda@gmail.com
 */
public class MainCoso {

    private static ConnectionFactory postman;
    private static Connection connection;
    private static Channel channel;
    public static boolean verbose = false;
    private static void send(String message, String queueName,String ipHost) throws Exception {
        channel.basicPublish("", queueName, null, message.getBytes());
    }
    private static String receive(String queueName,String ipHost) throws IOException, TimeoutException {
        if(verbose) System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

        AtomicReference<String> message = null;
        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            message.set(new String(delivery.getBody(), StandardCharsets.UTF_8));
            if(verbose) System.out.println(" [x] Received '" + message + "'");
        };
        channel.basicConsume(queueName, true, deliverCallback, consumerTag -> { });
        return message.get();
    }



    public static void main(String[] args) throws Exception {
        String ipHost = "localhost",message,queueName="Esplorazione";
        postman = new ConnectionFactory();
        connection = postman.newConnection("amqp://guest:guest@"+ipHost+":5672/");
        channel = connection.createChannel();
        channel.queueDeclare("Esplorazione", false, false, false, null);
        for(String arg:args){
            if (arg.equals("-v"))
                verbose = true;
            if(arg.equals("-h")){
                System.out.println("Usage: java -jar pacco.jar [-v] [-h]");
                System.out.println("-v: verbose mode");
                System.out.println("-h: help");
                System.exit(0);
                channel.close();
                connection.close();
            }
        }
        Esploratore esploratore = new Esploratore();


        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                try {
                    Thread.sleep(200);
                    System.out.println("Shutting down ...");
                    channel.close();
                    connection.close();

                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    e.printStackTrace();
                } catch (IOException | TimeoutException e) {
                    throw new RuntimeException(e);
                }
            }
        });


        while(true) {
            try{
                message = receive(queueName,ipHost);
                if(message.startsWith("Esplora:")) {
                    switch (message.substring(8)) {
                        case "m"://movements
                            switch (message.substring(9)) {
                                case "1" -> esploratore.right();
                                case "0" -> esploratore.forward();
                                case "2" -> esploratore.left();
                            }
                        case "u"://unknown, track to U
                            int[] U = esploratore.getMovements();
                            String U_string = "";
                            for (int j : U) {
                                U_string += j;
                                U_string += ",";
                            }
                            send(U_string, queueName,ipHost);
                        case "f"://flags, qualcosa con le flag
                            switch (message.charAt(9)) {
                                case 'd' -> esploratore.setDanger(5);
                                case 'c' -> esploratore.setLastCheckpoint();
                                case 'g' -> esploratore.goToCheckpoint();
                            }
                            break;
                        case "w"://wall
                            esploratore.setWall(Integer.parseInt(message.substring(9,10)),message.charAt(10)=='1');
                            break;
                    }
                }
                if(verbose) System.out.println(esploratore);

            }catch (Exception e){
                if(verbose) System.out.println("Errore di connessione");   //se non riesce a connettersi al broker
            }
        }



    }
}
