
ps x | grep '/data/Projects/or-eta-test/target/app_buddaa.jar' | grep -v grep | awk '{print $1}' | xargs kill -9
