package task;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map.Entry;
import java.util.Set;
import task.crossvalidation.DataSplitter;
import task.evaluating.UnrangedMetrics;
import task.learning.Acceptability;
import task.learning.assoc_rules_classif.AssociationRulesOnExtremums;
import task.learning.Classificator;
import task.learning.Element;
import task.utils.Utils;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class Task {
    public static abstract class Consts{
        public static final int SYMBOLS_AFTER_COMMA = 3;
        public static final String INPUT = "../../data_sets/cars/car.data";
        public static final int SIZE = 1728;
        public static final String DELIMITER = ",";
        public static final int CROSSVAL_CNT = 10;
    }
    
    private static Acceptability classification(Set<Classificator> classificators){
        EnumMap<Acceptability, Integer> implications = new EnumMap(Acceptability.class);
        Utils.initEnumMap(implications, 0);
        for(Classificator cl: classificators){
            if(cl.isImplication()){
                implications.put(cl.getImplicationGoal(), implications.get(cl.getImplicationGoal()) + 1);
            }
        }
        int max = 0;
        Acceptability result = Acceptability.UNACC;
        for(Entry<Acceptability, Integer> entry: implications.entrySet()){
            if(entry.getValue() > max){
                max = entry.getValue();
                result = entry.getKey();
            }
        }
        //если не нашли ни одной импликации
        if(Utils.mapIsEmpty(implications)){
            EnumMap<Acceptability, AssociationRulesOnExtremums> assocRules = new EnumMap(Acceptability.class);
            Utils.initEnumMap(assocRules, new AssociationRulesOnExtremums());
            //считаем максимальные коэффициенты по ассоциативным правилам
            for(Classificator cl: classificators){
                if(!cl.isImplication()){
                    for(Entry<Acceptability, AssociationRulesOnExtremums> entry: assocRules.entrySet()){
                        entry.getValue().takeIntoAccount(cl, entry.getKey());
                    }
                }
            }
            /*Сравниваем сначала по достоверности. Если макс. достоверность правил 
            для какого-то значения целевого признака оказалась наибольшей, это значение
            признака и будет результатом. Если таких наибольших несколько, сравниваем
            ещё и по макс. поддержке.
            Если значений целевого признака снова получилось несколько, сравниваем их 
            по мин. мощности ассоц. правил. Далее - просто по количеству.
            */
            for(int i = 0; i<AssociationRulesOnExtremums.COEFS_CNT; i++){
                double maxCoef = 0.0;
                for(Entry<Acceptability, AssociationRulesOnExtremums> entry: assocRules.entrySet()){
                    if(entry.getValue().getCoef(i) > maxCoef){
                        maxCoef = entry.getValue().getCoef(i);
                    }
                }
                List<Acceptability> sameList = new ArrayList<>();
                for(Entry<Acceptability, AssociationRulesOnExtremums> entry: assocRules.entrySet()){
                    if(entry.getValue().getCoef(i) == maxCoef){
                        sameList.add(entry.getKey());
                    }
                }
                if(sameList.size() == 1){
                    if(sameList.get(0) != Acceptability.UNACC){
                        System.out.println("Yes!");
                    }
                    return sameList.get(0);
                }
            }
        }
        return result;
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        List<Element> elements = new ArrayList<>();
        List<UnrangedMetrics> unrangedMetricses = new ArrayList<>();
        for(int i=0; i<Consts.CROSSVAL_CNT; i++){
            UnrangedMetrics unrangedMetrics = new UnrangedMetrics();
            int[] testIndexes = DataSplitter.getInstance().generateIndexes();
            int elementCnt = 0;
            try(RandomAccessFile rsf = new RandomAccessFile(Consts.INPUT, "r")){
                String line = null;
                //обучение
                while((line = rsf.readLine()) != null){
                    if(elementCnt <= testIndexes[0] || elementCnt > testIndexes[1]){
                        elements.add(new Element(line));
                    }
                    elementCnt++;
                }
                elementCnt = 0;
                rsf.seek(0);
                //тестировка
                Classificator.setTrainingDataSize(elements.size());
                while((line = rsf.readLine()) != null){
                    if(elementCnt > testIndexes[0] && elementCnt <= testIndexes[1]){
                        Element newEl = new Element(line);
                        //построение классификаторов
                        Set<Classificator> classificators = new HashSet<>();
                        for(Element el: elements){
                            Classificator cl = newEl.intersect(el);
                            for(Element e: elements){
                                if(!e.equals(el)){
                                    cl.add(e.contains(cl));
                                }
                            }
                            if(!cl.isEmpty()){
                                classificators.add(cl);
                            }
                        }
                        //классификация
                        unrangedMetrics.takeIntoAccount(classification(classificators), newEl.getAcceptability());
                        //дообучение
                        elements.add(newEl);
                    }
                    elementCnt++;
                }
                elements.clear();
                unrangedMetricses.add(unrangedMetrics);
            }
            catch(IOException ex){
                System.err.println("Unable to read the file!" + elementCnt);
            }
        }
        System.out.println(UnrangedMetrics.listToString(unrangedMetricses));
        System.out.println("******* AVERAGE *************");
        System.out.println(UnrangedMetrics.avg(unrangedMetricses).toString(false));
    }
}