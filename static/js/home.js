
$(document).ready(function() {

    // page is now ready, initialize the calendar...

    $('#calendar').fullCalendar(
        {   
            // dayClick: function() {
            //     alert('a day has been clicked!');
            // },
            height: 550,
            eventLimit: 3,
            events: [
                {
                    title  : 'event1',
                    start  : '2017-09-08'
                },
                {
                    title  : 'event2',
                    start  : '2017-09-08'
                },
                {
                    title  : 'event3',
                    start  : '2017-09-08'
                },
                {
                    title  : 'event4',
                    start  : '2017-09-08'
                },
                {
                    title  : 'event5',
                    start  : '2017-09-08'
                },
                {
                    title  : 'event2',
                    start  : '2017-09-10',
                    end    : '2017-09-11'
                },
                {
                    title  : 'event3',
                    start  : '2017-09-23',  
                    color  : 'yellow',
                    teste  : 'teste',
                    rodrigo: 'miguel'
                },
            ],
        });

    // $('#inserir').click(function() {
    //     var desc = prompt("Insira a descrição da transação");
    //     var data = prompt("Insira a data");
    //     var dia = data.substring(0, 2);
    //     var mes = data.substring(3, 5);
    //     var ano = data.substring(6);
    //     var dataFinal = ano + "-" + mes + "-" + dia;

    //     var string1 = 'Testando inserir evento';
    //     var teste = 
    //                 {
    //                     title  : desc,
    //                     start  : dataFinal,
    //                     color: 'yellow',   // an option!
    //                     textColor: 'black' // an option!
    //                 }

          
        
    //     $('#calendar').fullCalendar('renderEvent', teste);
    //     console.log(teste.desc);
    // });

});