package task.crossvalidation;

import java.util.Random;
import task.Task;
import task.Task.Consts;
/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class DataSplitter {
    private static final Random RANDOM = new Random(System.currentTimeMillis());
    private static DataSplitter instance;
    
    private DataSplitter(){
    }
    
    public static DataSplitter getInstance(){
        if(instance == null){
            instance = new DataSplitter();
        }
        return instance;
    }
    
    public int[] generateIndexes(){
        int testingSetDim = Task.Consts.SIZE / 10 + 1;
        int startIndex = RANDOM.nextInt(Consts.SIZE - testingSetDim);
        return new int[]{
            startIndex, 
            startIndex + testingSetDim
        };
    }
}
