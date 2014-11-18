
package task.evaluating;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 * @deprecated 
 */
public class AverageValues {
    private int sum;
    private int cnt;
    
    public AverageValues(){
        cnt = 0;
        sum = 0;
    }
    
    public void add(int value){
        sum += value;
        cnt++;
    }
    
    public double avg(){
        return (double)sum / cnt;
    }
}
