package bookTrading;

import java.awt.BorderLayout;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.*;

public class BookBuyerGui extends JFrame {
    private final JTextField title = new JTextField(22);
    private final JButton buy = new JButton("Купить");
    private final JTextArea status = new JTextArea(12, 48);
    private boolean stopped;

    public BookBuyerGui(BookBuyerAgent buyer, String initialTitle) {
        super("Покупатель: " + buyer.getLocalName());
        JPanel input = new JPanel();
        input.add(new JLabel("Книга:")); input.add(title); input.add(buy);
        title.setText(initialTitle);
        title.setEnabled(initialTitle.isEmpty());
        buy.setEnabled(initialTitle.isEmpty());
        status.setEditable(false);
        status.setLineWrap(true); status.setWrapStyleWord(true);
        JPanel content = new JPanel(new BorderLayout(8, 8));
        content.setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));
        content.add(input, BorderLayout.NORTH);
        content.add(new JScrollPane(status), BorderLayout.CENTER);
        content.add(new JLabel("Пример: Java_programming. Поиск повторяется каждые 5 секунд."), BorderLayout.SOUTH);
        buy.addActionListener(event -> {
            String name = title.getText().trim();
            if (name.isEmpty() || name.chars().anyMatch(Character::isWhitespace)) {
                JOptionPane.showMessageDialog(this, "Введите название без пробелов, например Java_programming.");
                return;
            }
            title.setEnabled(false); buy.setEnabled(false);
            buyer.requestPurchase(name);
        });
        title.addActionListener(event -> { if (buy.isEnabled()) buy.doClick(); });
        setContentPane(content);
        setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent event) {
                if (!stopped) buyer.doDelete();
                dispose();
            }
        });
        pack(); setLocationByPlatform(true);
    }

    public void appendStatus(String message) {
        status.append(message + "\n");
        status.setCaretPosition(status.getDocument().getLength());
    }

    public void agentStopped() {
        stopped = true;
        title.setEnabled(false); buy.setEnabled(false);
        appendStatus("Агент завершил работу. Окно можно закрыть.");
    }
}
