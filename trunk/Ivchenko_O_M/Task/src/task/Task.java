package task;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map.Entry;
import java.util.Random;
import java.util.Set;
import task.crossvalidation.DataSplitter;
import task.evaluating.RangedMetrics;
import task.evaluating.UnrangedMetrics;
import task.learning.Acceptability;
import task.learning.Classificator;
import task.learning.Element;
import task.learning.assoc_rules_classif.AssociationRules;
import task.learning.assoc_rules_classif.AssociationRulesOnCnt;
import task.learning.assoc_rules_classif.AssociationRulesOnExtremums;
import task.utils.Utils;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class Task {
    public static abstract class Consts{
        public static final Random RANDOM = new Random(System.currentTimeMillis());
        public static final int SYMBOLS_AFTER_COMMA = 3;
        public static final String INPUT = "../../data_sets/cars/car.data";
        public static final int SIZE = 1728;
        public static final String DELIMITER = ",";
        public static final int CROSSVAL_CNT = 10;
    }
    
    private static Acceptability classificationImplic(Set<Classificator> classificators){
        EnumMap<Acceptability, Integer> implications = new EnumMap(Acceptability.class);
        Utils.initEnumMap(implications, 0);
        for(Classificator cl: classificators){
            if(cl.isImplication()){
                implications.put(cl.getImplicationGoal(), implications.get(cl.getImplicationGoal()) + 1);
            }
        }
        int max = 0;
        Acceptability result = null;
        for(Entry<Acceptability, Integer> entry: implications.entrySet()){
            if(entry.getValue() > max){
                max = entry.getValue();
                result = entry.getKey();
            }
        }
        return result;
    }
    
    private static Acceptability classificationOnExtr(Set<Classificator> classificators){
        Acceptability result = classificationImplic(classificators);
        if(result != null){
            return result;
        }
        //если не нашли ни одной импликации
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
            for(Entry<Acceptability, AssociationRulesOnExtremums> entry: assocRules.entrySet()){
                if(entry.getValue().getCoef(i) != maxCoef){
                    assocRules.remove(entry.getKey());
                }
            }
            if(assocRules.size() == 1){
                assocRules.keySet().iterator().next();
            }
        }
        if(assocRules.size() != 1){
            int index = Consts.RANDOM.nextInt(assocRules.size());
            int ind = 0;
            Iterator<Acceptability> it = assocRules.keySet().iterator();
            while(it.hasNext() && ind <= index){
                result = it.next();
                ind++;
            }
        }
        return result;
    }
    
    private static Acceptability classificationOnCnt(Set<Classificator> classificators, double lim){
        Acceptability result = classificationImplic(classificators);
        if(result != null){
            return result;
        }
        //если не нашли ни одной импликации
        EnumMap<Acceptability, AssociationRulesOnCnt> assocRules = new EnumMap(Acceptability.class);
        Utils.initEnumMap(assocRules, new AssociationRulesOnCnt(lim));
        //считаем максимальные коэффициенты по ассоциативным правилам
        for(Classificator cl: classificators){
            if(!cl.isImplication()){
                for(Entry<Acceptability, AssociationRulesOnCnt> entry: assocRules.entrySet()){
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
            for(Entry<Acceptability, AssociationRulesOnCnt> entry: assocRules.entrySet()){
                if(entry.getValue().getCoef(i) > maxCoef){
                    maxCoef = entry.getValue().getCoef(i);
                }
            }
            for(Entry<Acceptability, AssociationRulesOnCnt> entry: assocRules.entrySet()){
                if(entry.getValue().getCoef(i) != maxCoef){
                    assocRules.remove(entry.getKey());
                }
            }
            if(assocRules.size() == 1){
                assocRules.keySet().iterator().next();
            }
        }
        if(assocRules.size() != 1){
            int index = Consts.RANDOM.nextInt(assocRules.size());
            int ind = 0;
            Iterator<Acceptability> it = assocRules.keySet().iterator();
            while(it.hasNext() && ind <= index){
                result = it.next();
                ind++;
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
        List<RangedMetrics> rangedMetricses = new ArrayList<>();
        for(int i=0; i<Consts.CROSSVAL_CNT; i++){
            UnrangedMetrics unrangedMetrics = new UnrangedMetrics();
            RangedMetrics rangedMetrics = new RangedMetrics();
            int[] testIndexes = DataSplitter.getInstance().generateIndexes();
            //System.out.println(testIndexes[0] + " " + testIndexes[1]);
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
                        Acceptability classificationRes = classificationOnExtr(classificators);
                        //оценка алгоритма
                        unrangedMetrics.takeIntoAccount(classificationRes, newEl.getAcceptability());
                        rangedMetrics.takeIntoAccount(classificationRes, newEl.getAcceptability());
                        //дообучение
                        elements.add(newEl);
                    }
                    elementCnt++;
                }
                elements.clear();
                unrangedMetricses.add(unrangedMetrics);
                rangedMetricses.add(rangedMetrics);
            }
            catch(IOException ex){
                System.err.println("Unable to read the file!" + elementCnt);
            }
        }
        System.out.println(UnrangedMetrics.listToString(unrangedMetricses));
        System.out.println("******* AVERAGE *************");
        System.out.println(UnrangedMetrics.avg(unrangedMetricses).toString(false));
        System.out.println("");
        System.out.println(RangedMetrics.listToString(rangedMetricses));
        System.out.println("******* AVERAGE *************");
        System.out.println(RangedMetrics.avg(rangedMetricses).toString(false));
    }
}