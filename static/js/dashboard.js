const ctx = document.getElementById('grafico').getContext('2d');
const ctx2 = document.getElementById('doughnut').getContext('2d');
var myChart;
var select_data = 0;
var hide_data = 1;

function gera_cor(qtd=1){
    var bg_color = []
    var border_color = []
    for(let i = 0; i < qtd; i++){
        let r = Math.random()*255;
        let g = Math.random()*255;
        let b = Math.random()*255;

        bg_color.push(`rgba(${r}, ${g}, ${b}, ${0.7})`)
        border_color.push(`rgba(${r}, ${g}, ${b}, ${1})`)

    }
    
    return [bg_color,border_color];
}


function renderiza_doughnut(url){
    
    fetch(url,{
        method:'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

    
    var cores = gera_cor(qtd=12);

    const ChartDoughnut = new Chart(ctx2,{
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets:[{
                data: data.data,
                backgroundColor: ["#003f5c",
                "#2f4b7c",
                "#665191",
                "#a05195",
                "#d45087",
                "#f95d6a",
                "#ff7c43",
                "#ffa600"],
                                
            }]
        },

    });
})
}



function renderiza_grafico(url){
    if (myChart !== undefined){
        myChart.destroy()
    }
    fetch(url,{
        method:'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

    
    var cores = gera_cor(qtd=12);

    window.myChart = new Chart(ctx,{
        type: 'line',
        data: {
            labels: data.labels,
            datasets:[{
                label: 'Empréstimos',
                data: data.data,
                backgroundColor: "rgba(0, 63, 92, 0.5)",
                borderColor: "rgba(0, 63, 92, 0.9)",
                pointStyle: 'circle',
                pointRadius: 10,
                pointHoverRadius: 15
            },
            {
                label: 'Usuários',
                data: data.data_usuario,
                backgroundColor: "rgb(255, 166, 0, 0.5)",
                borderColor: "rgba(255, 166, 0, 0.9)",
                pointStyle: 'circle',
                pointRadius: 10,
                pointHoverRadius: 15
            }
        
        ]
        },

        options: {
            responsive: true,
            plugins: {
              title: {
                display: true,
                text: 'Empréstimos no último ano',
                color: "#000000",
                font: {
                    size: 20,
                    
                  }
              },
            }},
    });
    
    myChart.hide(hide_data);
})
}


function filtra_grafico_semestre(url){
    fetch(url,{
        method:'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
    myChart.data.labels = myChart.data.labels.slice(6,12);
    myChart.data.datasets[0].data = myChart.data.datasets[select_data].data.slice(6,12);
    myChart.options.plugins.title.text = 'Empréstimos no último semestre'
    myChart.update();
    console.log(myChart.data.datasets[0].data);

    })
}


function updateChart(dataset){
    const isDataShown = myChart.isDatasetVisible(dataset.value);
    console.log(isDataShown)

    if (dataset.value === '0'){
        select_data = 0
        hide_data = 1
        myChart.show(0);
        myChart.hide(1);
        console.log('Emprestimos selecionado')
    }
    if (dataset.value === '1'){
        select_data = 1
        hide_data = 0
        myChart.show(1);
        myChart.hide(0);
        console.log('Usuarios selecionado')
    }

    // if (isDataShown === false){
    //     myChart.show(dataset.value);
    // }
    // if (isDataShown === true){
    //     myChart.hide(dataset.value);

// }
}