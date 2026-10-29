package bookTrading;

import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.Behaviour;
import jade.core.behaviours.OneShotBehaviour;
import jade.core.behaviours.TickerBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;
import java.awt.GraphicsEnvironment;
import javax.swing.SwingUtilities;

public class BookBuyerAgent extends Agent {
    private String title;
    private boolean purchasing;
    private BookBuyerGui gui;

    protected void setup() {
        Object[] args = getArguments();
        boolean hasTitle = args != null && args.length > 0 && !args[0].toString().isBlank();
        if (!GraphicsEnvironment.isHeadless()) {
            String initialTitle = hasTitle ? args[0].toString() : "";
            SwingUtilities.invokeLater(() -> {
                gui = new BookBuyerGui(this, initialTitle);
                gui.setVisible(true);
            });
        }
        if (!hasTitle && GraphicsEnvironment.isHeadless()) {
            System.out.println(getLocalName() + ": specify book title in Arguments.");
            doDelete(); return;
        }
        title = hasTitle ? args[0].toString() : null;
        report(hasTitle ? "Ищу книгу: " + title : "Введите название книги и нажмите «Купить».");
        // Пауза даёт время включить наблюдение в Sniffer. Новая попытка каждые 5 секунд.
        addBehaviour(new TickerBehaviour(this, 5000) {
            protected void onTick() {
                if (purchasing || title == null) return;
                DFAgentDescription template = new DFAgentDescription();
                ServiceDescription service = new ServiceDescription();
                service.setType("book-selling"); template.addServices(service);
                try {
                    DFAgentDescription[] sellers = DFService.search(myAgent, template);
                    System.out.println(getLocalName() + " searching " + title + "; sellers=" + sellers.length);
                    report("Поиск «" + title + "». Продавцов: " + sellers.length);
                    if (sellers.length > 0) {
                        purchasing = true;
                        addBehaviour(new RequestPerformer(sellers));
                    }
                } catch (FIPAException ex) { ex.printStackTrace(); }
            }
        });
    }

    public void requestPurchase(String requestedTitle) {
        addBehaviour(new OneShotBehaviour() {
            public void action() {
                if (title != null || purchasing) return;
                title = requestedTitle;
                report("Ищу книгу: " + title + ". Опрос каждые 5 секунд.");
            }
        });
    }

    private void report(String message) {
        SwingUtilities.invokeLater(() -> { if (gui != null) gui.appendStatus(message); });
    }

    private class RequestPerformer extends Behaviour {
        private final Set<AID> pending = new HashSet<>();
        private AID bestSeller;
        private int bestPrice = Integer.MAX_VALUE;
        private int step;
        private long deadline;
        private MessageTemplate replies;

        RequestPerformer(DFAgentDescription[] sellers) {
            for (DFAgentDescription seller : sellers) pending.add(seller.getName());
        }

        public void action() {
            switch (step) {
                case 0 -> {
                    ACLMessage cfp = new ACLMessage(ACLMessage.CFP);
                    for (AID seller : pending) cfp.addReceiver(seller);
                    cfp.setContent(title); cfp.setConversationId("book-trade");
                    cfp.setReplyWith(UUID.randomUUID().toString());
                    replies = matching(cfp);
                    send(cfp); deadline = System.currentTimeMillis() + 3000; step = 1;
                }
                case 1 -> {
                    ACLMessage reply = receive(replies);
                    if (reply != null && pending.remove(reply.getSender())
                            && reply.getPerformative() == ACLMessage.PROPOSE) {
                        try {
                            int price = Integer.parseInt(reply.getContent());
                            report(reply.getSender().getLocalName() + " предлагает цену " + price);
                            if (price > 0 && (bestSeller == null || price < bestPrice)) {
                                bestPrice = price; bestSeller = reply.getSender();
                            }
                        } catch (NumberFormatException ignored) { }
                    }
                    if (pending.isEmpty() || System.currentTimeMillis() >= deadline) {
                        if (bestSeller == null) {
                            System.out.println(getLocalName() + ": no offers for " + title); step = 3;
                            report("Книги нет в наличии. Повторю поиск через 5 секунд.");
                        } else {
                            ACLMessage order = new ACLMessage(ACLMessage.ACCEPT_PROPOSAL);
                            order.addReceiver(bestSeller); order.setContent(title);
                            order.setConversationId("book-trade");
                            order.setReplyWith(UUID.randomUUID().toString());
                            replies = MessageTemplate.and(matching(order), MessageTemplate.MatchSender(bestSeller));
                            send(order); deadline = System.currentTimeMillis() + 3000; step = 2;
                            report("Выбран " + bestSeller.getLocalName() + ", цена " + bestPrice + ". Отправлен заказ.");
                        }
                    } else if (reply == null) block(Math.max(1, deadline - System.currentTimeMillis()));
                }
                case 2 -> {
                    ACLMessage result = receive(replies);
                    if (result != null) {
                        if (result.getPerformative() == ACLMessage.INFORM) {
                            System.out.println(getLocalName() + " BOUGHT " + title + " from "
                                + bestSeller.getLocalName() + " price=" + bestPrice);
                            doDelete();
                            report("Куплено: " + title + " у " + bestSeller.getLocalName() + " за " + bestPrice);
                        } else {
                            System.out.println(getLocalName() + ": purchase failed, will retry.");
                            report("Книга уже продана или заказ отклонён. Повторю поиск.");
                        }
                        step = 3;
                    } else if (System.currentTimeMillis() >= deadline) {
                        // Не повторяем заказ: продавец мог продать книгу, но ответ не дошёл.
                        System.out.println(getLocalName() + ": order confirmation timed out; outcome unknown.");
                        report("Подтверждение не получено. Результат заказа неизвестен.");
                        step = 3; doDelete();
                    } else block(Math.max(1, deadline - System.currentTimeMillis()));
                }
            }
        }

        private MessageTemplate matching(ACLMessage message) {
            return MessageTemplate.and(MessageTemplate.MatchConversationId("book-trade"),
                MessageTemplate.MatchInReplyTo(message.getReplyWith()));
        }
        public boolean done() { return step == 3; }
        public int onEnd() { purchasing = false; return 0; }
    }

    protected void takeDown() {
        System.out.println(getLocalName() + " terminating.");
        SwingUtilities.invokeLater(() -> { if (gui != null) gui.agentStopped(); });
    }
}
