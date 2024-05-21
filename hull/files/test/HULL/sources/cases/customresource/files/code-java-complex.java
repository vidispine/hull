import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;


public class FreqTableExampleOriginal {

    public static final int NUM_ASCII_CHAR = 128;

    // program to create a frequency table.
    // Example of simple try catch blocks to deal with checked exceptions
    public static void main(String[] args)
        {

        int[] freqs = createFreqTableURL("http://www.utexas.edu/");

        if( freqs.length == 0)
            System.out.println("No frequency table created due to problems when reading from file");
        else{
            for(int i = 0; i < NUM_ASCII_CHAR; i++){
                System.out.println("charcater code: " + i + " ,character: " + (char)i + " ,frequency: " + freqs[i]);
            }
            System.out.println("Total characters in file: " + sum(freqs));
        }


        freqs = new int[]{};
        try{
            freqs = createTable("ciaFactBook2008.txt");
        }
        catch(FileNotFoundException e){
            System.out.println("File not found. Unable to create freq table" + e);
        }
        catch(IOException e){
            System.out.println("Problem while reading from file. Unable to create freq table" + e);
        }
        if( freqs.length == 0)
            System.out.println("No frequency table created due to problems when reading from file");
        else{
            for(int i = 0; i < freqs.length; i++){
                System.out.println("charcater code: " + i + " ,character: " + (char)i + " ,frequency: " + freqs[i]);
            }
            System.out.println("Total characters in file: " + sum(freqs));
        }

    }


    // return sum of ints in list
    // list may not be null
    private static int sum(int[] list) {
        assert list != null : "Failed precondition, sum: parameter list" +
            " may not be null.";
        int total = 0;
        for(int x : list){
            total += x;
        }
        return total;
    }


    // pre: url != null
    // Connect to the URL specified by the String url.
    // Map characters to index in array.
    // All non ASCII character dumped into one element of array
    // If IOException occurs message printed and array of
    // length 0 returned.
    public static int[] createFreqTableURL (String url){
        if(url == null)
            throw new IllegalArgumentException("Violation of precondition. parameter url must not be null.");

        int[] freqs = new int[NUM_ASCII_CHAR];
        try {
        URL inputURL = new URL(url);
        InputStreamReader in
            = new InputStreamReader(inputURL.openStream());

        while(in.ready()){
            int c = in.read();
            if(0 <= c && c < freqs.length)
                freqs[c]++;
            else
                System.out.println("Non ASCII char: " + c + " " + (char) c);
        }
        in.close();
        }
        catch(MalformedURLException e){
            System.out.println("Bad URL.");
            freqs = new int[0];
        }
        catch(IOException e){
            System.out.println("Unable to read from resource." + e);
            freqs = new int[0];
        }
        return freqs;
    }



    // Connect to the file specified by the String fileName.
    // Assumes it is in same directory as compiled code.
    // Map characters to index in array.
    public static int[] createTable(String fileName) throws FileNotFoundException, IOException{
        int[] freqs = new int[NUM_ASCII_CHAR];
        File f = new File(fileName);
        FileReader r = new FileReader(f);
        while( r.ready() ){
            int ch = r.read();
//            if( 0 <= ch && ch <= NUM_ASCII_CHAR)
//                freqs[ch]++;
//            else
//                freqs[INDEX_NON_ASCII]++;
            if(0 <= ch && ch < freqs.length)
                freqs[ch]++;
            else
                System.out.println((char) ch);
                
        }
        r.close();
        return freqs;
    }








}