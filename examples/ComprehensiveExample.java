/*
 * Comprehensive Java Example - Triggers All Metrics
 * This example demonstrates:
 * - Inheritance hierarchy (DIT, NOC)
 * - Complex control flow (CC, WMC)
 * - External type references (CBO)
 * - Various operators and operands (Halstead)
 * - Nested classes
 * - Multiple methods with varying complexity
 */

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.io.File;
import java.io.IOException;

// Base class - Level 0 (DIT = 0)
public class ComprehensiveExample {
    
    // External types for CBO
    private List<String> items;
    private Map<String, Integer> counts;
    private Scanner input;
    private File configFile;
    
    // Constructor
    public ComprehensiveExample() {
        this.items = new ArrayList<>();
        this.counts = new HashMap<>();
        this.input = new Scanner(System.in);
        this.configFile = new File("config.txt");
    }
    
    // Simple method (CC = 1)
    public void simpleMethod() {
        System.out.println("Simple method");
    }
    
    // Method with if-else (CC = 2)
    public int checkValue(int value) {
        if (value > 0) {
            return value * 2;
        } else {
            return 0;
        }
    }
    
    // Method with while loop (CC = 2)
    public void processItems() {
        int index = 0;
        while (index < items.size()) {
            String item = items.get(index);
            System.out.println("Processing: " + item);
            index++;
        }
    }
    
    // Method with for loop (CC = 2)
    public int calculateSum(int[] numbers) {
        int sum = 0;
        for (int i = 0; i < numbers.length; i++) {
            sum += numbers[i];
        }
        return sum;
    }
    
    // Method with logical operators (CC = 3: base + && + ||)
    public boolean validateInput(String input, int min, int max) {
        if (input != null && input.length() >= min && (input.length() <= max || input.equals("admin"))) {
            return true;
        }
        return false;
    }
    
    // Method with switch statement (CC = 1 + cases)
    public String processCommand(String command) {
        switch (command) {
            case "start":
                return "Starting...";
            case "stop":
                return "Stopping...";
            case "pause":
                return "Pausing...";
            case "resume":
                return "Resuming...";
            default:
                return "Unknown command";
        }
    }
    
    // Method with try-catch (CC = 2)
    public void readFile() {
        try {
            if (configFile.exists()) {
                System.out.println("File exists");
            }
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
    
    // Complex method with nested control flow (CC = 6: base + if + while + if + && + ||)
    public void complexProcessing(int[] data, int threshold) {
        int i = 0;
        while (i < data.length) {
            if (data[i] > threshold) {
                if (data[i] % 2 == 0 && (data[i] > 100 || data[i] < 1000)) {
                    System.out.println("Processing: " + data[i]);
                }
            }
            i++;
        }
    }
    
    // Method with ternary operator (CC = 2)
    public String getStatus(int value) {
        return value > 0 ? "Positive" : "Negative";
    }
    
    // Method with do-while (CC = 2)
    public void retryOperation() {
        int attempts = 0;
        do {
            attempts++;
            System.out.println("Attempt " + attempts);
        } while (attempts < 3);
    }
    
    // Nested class
    public static class Helper {
        private String name;
        
        public Helper(String name) {
            this.name = name;
        }
        
        public String getName() {
            return name;
        }
        
        // Method with if-else chain (CC = 4)
        public int categorize(int value) {
            if (value < 0) {
                return -1;
            } else if (value == 0) {
                return 0;
            } else if (value > 100) {
                return 2;
            } else {
                return 1;
            }
        }
    }
    
    public static void main(String[] args) {
        ComprehensiveExample example = new ComprehensiveExample();
        example.simpleMethod();
        example.checkValue(10);
        example.processItems();
        
        int[] numbers = {1, 2, 3, 4, 5};
        example.calculateSum(numbers);
        example.validateInput("test", 3, 10);
        example.processCommand("start");
        example.readFile();
        
        int[] data = {50, 150, 200, 500, 1200};
        example.complexProcessing(data, 100);
        example.getStatus(5);
        example.retryOperation();
    }
}

// Level 1 inheritance (DIT = 1)
class BaseProcessor extends ComprehensiveExample {
    
    private String processorName;
    
    public BaseProcessor(String name) {
        this.processorName = name;
    }
    
    // Override with additional complexity (CC = 3)
    @Override
    public void processItems() {
        super.processItems();
        if (items != null && !items.isEmpty()) {
            System.out.println("Processed " + items.size() + " items");
        }
    }
    
    // New method with for-each loop (CC = 2)
    public void processAll() {
        for (String item : items) {
            if (item != null) {
                System.out.println(item);
            }
        }
    }
}

// Level 2 inheritance (DIT = 2)
class AdvancedProcessor extends BaseProcessor {
    
    private int maxItems;
    
    public AdvancedProcessor(String name, int max) {
        super(name);
        this.maxItems = max;
    }
    
    // Complex method with multiple control structures (CC = 5)
    public void advancedProcessing() {
        int count = 0;
        for (int i = 0; i < items.size() && count < maxItems; i++) {
            String item = items.get(i);
            if (item != null && item.length() > 5) {
                System.out.println("Advanced: " + item);
                count++;
            }
        }
    }
    
    // Method with nested try-catch (CC = 3)
    public void safeOperation() {
        try {
            try {
                readFile();
            } catch (IOException e) {
                System.out.println("IO Error");
            }
        } catch (Exception e) {
            System.out.println("General Error");
        }
    }
}

// Another Level 1 class (for NOC testing)
class SimpleProcessor extends ComprehensiveExample {
    
    public void simpleProcess() {
        System.out.println("Simple processing");
    }
}

