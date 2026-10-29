package B;

import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;

public class BMain extends Agent {

    @Override
    protected void setup() {
        System.out.println("Привет! агент " + getAID().getName() + " готов.");
        addBehaviour(new CyclicBehaviour(this) {

            @Override
            public void action() {
                ACLMessage msg = receive();
                if (msg != null) {
                    ACLMessage reply = msg.createReply();
                    if (msg.getPerformative() == ACLMessage.REQUEST && "Ping".equals(msg.getContent())) {
                        System.out.printf("%s received Ping from %s%n",
                                getLocalName(), msg.getSender().getLocalName());
                        reply.setPerformative(ACLMessage.INFORM);
                        reply.setContent("Pong");
                    } else {
                        reply.setPerformative(ACLMessage.NOT_UNDERSTOOD);
                        reply.setContent("Expected REQUEST with content Ping");
                    }
                    send(reply);
                    System.out.printf("%s sent %s to %s%n",
                            getLocalName(), reply.getContent(), msg.getSender().getLocalName());
                } else {
                    block();
                }
            }
        });
    }
}
