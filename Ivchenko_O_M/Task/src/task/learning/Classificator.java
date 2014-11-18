
package task.learning;

import java.util.EnumMap;
import java.util.Map.Entry;
import task.utils.Utils;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class Classificator extends Element implements Comparable<Classificator>{
    private static int trainingDataSize; 
    private final EnumMap<Acceptability, Integer> map;
    private boolean isNew;
    private int cnt;
    private Acceptability implicAcceptability;
    
    public static void setTrainingDataSize(int dataSize){
        trainingDataSize = dataSize;
    }
    
    public Classificator(){
        super();
        map = new EnumMap(Acceptability.class);
        Utils.initEnumMap(map, 0);
        isNew = true;
        cnt = 0;
    }
    
    public boolean isImplication(){
        int nonZeroElsCnt = 0;
        for(Entry<Acceptability, Integer> entry: map.entrySet()){
            if(entry.getValue() != 0){
                implicAcceptability = entry.getKey();
                nonZeroElsCnt++;
            }
            if(nonZeroElsCnt > 1 || nonZeroElsCnt == 0){
                return false;
            }
        }
        return true;
    }
    
    public Acceptability getImplicationGoal(){
        return implicAcceptability;
    }
    
    public void add(Acceptability acceptability){
        if(acceptability != null){
            map.put(acceptability, map.get(acceptability) + 1);
            cnt++;
        }
    }
    
    @Override
    public String toString(){
        StringBuilder sb = new StringBuilder(super.toString());
        for(Entry<Acceptability, Integer> entry: map.entrySet()){
            sb.append(" (").append(entry.getKey().name()).append(", ");
            sb.append(entry.getValue()).append(")");
        }
        return sb.toString();
    }
    
    public int getPower(){
        int power = 0;
        for(Type t: enumCoeffs){
            if(t.isDefined()){
                power++;
            }
        }
        for(int v: intCoeffs){
            if(v != 0){
                power++;
            }
        }
        return power;
    }
    
    public double getConfidence(Acceptability acc){
        return (double)map.get(acc) / cnt;
    }
    
    public double getSupport(Acceptability acc){
        return (double)map.get(acc) / trainingDataSize;
    }

    @Override
    public int compareTo(Classificator cl) {
        boolean more = false;
        boolean less = false;
        for(int i=0; i<enumCoeffs.length; i++){
            if(cl.enumCoeffs[i].isDefined() && !enumCoeffs[i].isDefined()){
                more = true;
            }
            else if(!cl.enumCoeffs[i].isDefined() && enumCoeffs[i].isDefined()){
                less = true;
            }
        }
        for(int i=0; i<intCoeffs.length; i++){
            if(cl.intCoeffs[i] == 0 && intCoeffs[i] != 0){
                more = true;
            }
            else if(cl.intCoeffs[i] != 0 && intCoeffs[i] == 0){
                less = true;
            }
        }
        if((more && less) || (!more && !less)){
            return 0;
        }
        else if(more){
            return 1;
        }
        return -1;
    }
    
    public boolean isEmpty(){
        return cnt == 0;
    }
}
