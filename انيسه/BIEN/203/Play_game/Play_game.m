
%Developed by Dr. Kevin Holly
%for BIEN 203: Principals in Biomedical Engineering

Q1 = questdlg('Do you want to play a game?','Answer the question','Yes','No.','No.');

if Q1 == 'No.'
    
 Q1 = questdlg('Are you sure?','Please answer','Yes','No.','No.');
   if Q1 == 'No.'
      Q1 = questdlg('Ok, say yes then','Please say yes','Yes','No.','No.');
        if Q1 == 'No.'
        Q1 = questdlg('The ANSWER IS YES!!','I don''t like you...','Yes','No.','No.');
            if Q1 == 'No.'
                uiwait(msgbox('It''s over... YES! It is over.. Fear my wrath! There is a way to escape if you paid attention in class... MUAHAHHAHAHHAHAHHAHAHAA!','You lost the game... You should have said Yes'));
                figure('name','Should have said yes','units','normalized','outerposition',[.5 0 .5 .5])
                text(.5, .5, 'Too many Yes''s? Click here!', 'clipping', 'off');
                axis off
                figure('name','Should have said yes','units','normalized','outerposition',[.5 .5 .5 .5])
                axis off    
                for i = 1:1:1000000
                   axis off
                   disp('You should have said YES!!!!!') 
                   text(rand, rand, 'YES', 'clipping', 'off');
                   pause(.25)
                end
                end
            end
        end
   end
   

   uiwait(msgbox(["GREAT!!!! I KNEW YOU WOULD SAY YES!!!!";"";"I always wanted someone to play games with me!";"";"Let's play signal processing! This is the bestest game ever! Biomedical engineers love this game!"]))
   
   uiwait(msgbox(["First, we need to find a signal to analyze!                                        Where is it?";"";"                               *Searches for the signal*";"";"Oh! Here it is!"],'The signal processing game!'))
   disp('>>%Look at me!');
   pause(2)
   disp('>>%I''m typing in your command window!')
   pause(2)
   disp('>>%This is going to be Great!')
   pause(2)
   disp('>>%ooooOOOO! I can type commands too!')
   pause(2)
   disp('>>load(Data_of_the_best_signal_game_ever!)')
   load('Data_of_the_best_signal_game_ever!');
   pause(2)
   uiwait(msgbox(["Look at the workspace! There are two variables. One is called signal. I believe that is the signal. The other is called fs. I believe this stands for the frequency sampling rate. This may come in handy later...","","Interesting.. it looks like you can see my commands in the workspace as well"], "Best Signal Processing Game EVER!"))
   disp('>>')
   disp('>>')
   disp('>>')
   disp('>>')
   disp('>>')
   disp('>>%Ok! Let''s play Repeat after me!')
   pause(2)
   disp('>>%When I state a command, Type it! When I make a comment, Ignore it!')
   pause(2)
   disp('>>%Let''s start playing!')
   pause(2)
   figure(1)
   disp('>>plot(1:length(signal(1:15000)),signal(1:15000))')
   pause(2)
   uiwait(msgbox(["HINT!!";"";"Try typing the following in the command window:";"";"plot(1:length(signal(1:15000)),signal(1:15000))"],'HINT'))
   input('>>')
   figure(1)
   disp('>>title(''Unknown signal'')')
   input('>>')
   figure(1)
   disp('>>%This will take too long.. let me help out')
   pause(2)
   disp('>>%Ok, adding x and y labels')
   xlabel('Time (units unknown!)');
   pause(2)
   ylabel('Amplitude');
   pause(2)
   disp('>>%Changing background color')
   set(gcf,'color','w');
   pause(2)
   disp('>>%And adding a hold on')
   hold on
   pause(2)
   
% %    hold on
% %    stem(1,axis_handle.YLim(1),'m')
% %    stem(1,axis_handle.YLim(2),'m')
   
   disp('>>%Setting axis_handle = gca;')
   axis_handle = gca;
   pause(2)
   
   figure(1)
   disp('>>stem(1,axis_handle.YLim(1),''m'')')
   input('>>')
   figure(1)
   disp('>>stem(1,axis_handle.YLim(2),''m'')')
   input('>>')
   figure(1)
   
     
   
% %     %Try this:
% %     for i = 1:100:15000
% %     axis_handle.Children(1).XData = i;
% %     axis_handle.Children(2).XData = i;
% %     pause(1)
% %     end

   disp('>>%Try this:');
   disp('>>')
   disp('>>for i = 1:100:15000');
   disp('>>axis_handle.Children(1).XData = i;')
   disp('>>axis_handle.Children(2).XData = i;')
   disp('>>pause(1)');
   disp('>>end')
   
   msgbox(["You have now entered the open ended section of the signal processing game.";"";"Objective: Please consult with Dr. Holly about the next task. He will confirm your progress and provide the next command to move on."],'The Open-ended Signal Processing Game!');

   

   