
package task.utils;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.EnumMap;
import task.Task.Consts;
import task.learning.Acceptability;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public abstract class Utils {
    /**
     * Округление числа.
     * @param value дробное число.
     * @param symbolsAfterComma кол-во знаков после запятой в округлённом числе.
     * @return округлённое дробное число.
     */
    private static double roundDouble(double value, int symbolsAfterComma){
        return new BigDecimal(value).setScale(symbolsAfterComma, RoundingMode.HALF_UP).doubleValue();
    }
    
    public static double roundDouble(double value){
        return roundDouble(value, Consts.SYMBOLS_AFTER_COMMA);
    }
    
    public static <K extends Object> void initEnumMap(EnumMap<Acceptability, K> map, K defaultValue){
        for(Acceptability acceptability: Acceptability.values()){
            map.put(acceptability, defaultValue);
        }
    }
    
    public static boolean mapIsEmpty(EnumMap<Acceptability, Integer> map){
        for(Acceptability acceptability: Acceptability.values()){
            if(map.get(acceptability) != 0){
                return false;
            }
        }
        return true;
    }
    
//    public static <K extends Enum<K>> void initEnumMap(EnumMap<K, Integer> map){
//        for(K k: K.values()){
//            
//        }
//    }
}
