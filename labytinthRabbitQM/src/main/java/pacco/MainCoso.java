package pacco;

import com.rabbitmq.client.*;

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
 * @mail samuele.facenda@gmail.com
 */
public class MainCoso {

    private static ConnectionFactory postman;
    private static Connection connection;
    private static Channel channel;
    public static boolean verbose = false;

    private static final String queueName = "Esplorazione", ipHost = "127.0.0.1";

    private static Esploratore esploratore;
    private static void send(String message) throws Exception {
        channel.basicPublish("", queueName, null, message.getBytes());
    }
    private static void receive() throws IOException, TimeoutException {
        //if(verbose) System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

        DeliverCallback deliverCallback = MainCoso::messageCallback;
        channel.basicConsume(queueName, true, deliverCallback, consumerTag -> { });
    }

    private static void recive(){
        try{
            receive();
        }catch (TimeoutException e){
            recive();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void messageCallback(String consumerTag, Delivery delivery) {

        recive();

        String message = new String(delivery.getBody(), StandardCharsets.UTF_8);
        if(!message.equals("")){
            System.out.println("message: " + message);
            if (message.startsWith("Esplora:")) {
                switch (message.substring(8,9)) {
                    case "m"://movements
                        switch (message.substring(9)) {
                            case "1" -> esploratore.right();
                            case "0" -> esploratore.forward();
                            case "3" -> esploratore.left();
                            case "2" -> esploratore.back();
                        }
                    case "u"://unknown, track to U
                        int[] U = esploratore.getMovements();
                        String U_string = "";
                        for (int j : U) {
                            U_string += j;
                            U_string += ",";
                        }
                        if(verbose) System.out.println("U: " + U_string);
                        try {
                            try{
                                U_string = U_string.substring(0, U_string.length() - 1);
                            }catch (Exception e){
                                U_string = "";
                            }
                            send(U_string);
                            System.out.println("U sent");
                        } catch (Exception e) {
                            throw new RuntimeException(e);
                        }
                    case "f"://flags, qualcosa con le flag
                        switch (message.charAt(9)) {
                            case 'd' -> esploratore.setDanger(5);
                            case 'c' -> esploratore.setLastCheckpoint();
                            case 'g' -> esploratore.goToCheckpoint();
                        }
                        break;
                    case "w"://wall
                        esploratore.setWall(Integer.parseInt(message.substring(9, 10)), message.charAt(10) == '1');
                        break;
                }
            }
            if(verbose) System.out.println(esploratore);
        }

    }

    public static void main(String[] args) throws Exception {
        postman = new ConnectionFactory();
        connection = postman.newConnection("amqp://guest:guest@"+ipHost+":15672/");
        channel = connection.createChannel();
        channel.queueDeclare("Esplorazione", true, false, false, null);
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
        esploratore = new Esploratore();


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

        recive();

    }
}
