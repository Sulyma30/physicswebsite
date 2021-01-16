//It creates info about the theme and here we should use url_for and transfer parameters (theme_id and type: theory or exp) so we can open the page with selected theme by clicking on the corresponding button
class MaterialInfo extends React.Component {
    constructor(props) {
        super(props);
        this.setSelected = this.setSelected.bind(this);
    }
    setSelected(sel_title, e) {
        this.props.setSelected("theme", sel_title);
    }
    render() {
        const theme = this.props.theme;
        const requirements = [];
        theme.requirements.map((requirement) => {
            requirements.push(
                <a href="#" key={requirement} className="d-inline-block text-truncate mx-1" onClick={(e) => this.setSelected(requirement, e)} >{requirement} </a>
            );
        });
        return(
            <div id="material-info" className="d-flex flex-column pt-md-4 align-items-center my-4">
                <div className="h1 text-center">{theme.title}</div>
                { theme.requirements.length !== 0 ?
                    <div className="row d-flex justify-content-center pt-3 border-top">
                        <div className="font-weight-bold pr-3">Корисно знати: </div>
                        {requirements}
                    </div>
                : null
                }
                <div className="row mt-3">
                    <div className="col-6">
                        <a href={"/material/" + theme.id + "/problems"} className="btn btn-outline-bg waves-effect text-nowrap"><span className="d-none d-sm-block">Розв'язувати задачі</span><span className="d-sm-none">Задачі</span></a> 
                    </div>
                    <div className="col-6">
                        <a href={"/material/" + theme.id + "/theory"}  className="btn btn-outline-bg waves-effect text-nowrap"><span className="d-none d-sm-block">Читати теорію</span><span className="d-sm-none">Теорія</span></a> 
                    </div>
                </div>
            </div>
        );
    }
}

class SelectorOption extends React.Component {
    constructor(props){
        super(props);
        this.setSelected = this.setSelected.bind(this);
    }
    setSelected(e) {
        this.props.setSelected(this.props.option);
    }
    render() {
        var optionStyle = "text-center waves-effect selector-option "
        switch (this.props.optionType) {
            case "active" :
                optionStyle += " btn-lg py-3 list-group-item-action list-group-item-light black-text ";
                break;
            case "selected" :
                optionStyle += " btn-sm my-0 py-sm-2 py-1 list-group-item-action list-group-item-light black-text active";
                break;
            default:
                optionStyle += " d-none d-sm-block btn-sm my-0 py-2  grey-text"
        }
        return(
            <div key={this.props.option} className={optionStyle} id={this.props.option} onClick={(e) => this.setSelected(e)}>
                {this.props.option}
            </div>
        );
    }
}

class Selector extends React.Component {
    constructor(props) {
        super(props);
        this.setSelected = this.setSelected.bind(this);
    }
    setSelected(sel_title, e) {
        if (this.props.sel_title === sel_title){
            this.props.setSelected("", "");
        }
        else {
            this.props.setSelected(this.props.type, sel_title);
        }
    }
    render() {
        if (this.props.options.length === 0){
            return null;
        }
        const list = [];
        this.props.options.map((option) => {
            var optionType = "";
            if (this.props.sel_title === ""){
                optionType = "active";
            }
            else if (this.props.sel_title === option){
                optionType = "selected";
            }
            list.push(<SelectorOption option={option} key={option} setSelected={this.setSelected} optionType={optionType} />)
        });
        return(
            <div className={'col-12 col-sm-4 mb-1 d-flex flex-column selector-column list-group ' + (this.props.sel_title === "" ? 'active-column px-0 mx-0' : 'px-1 mx-0')} >
                {list}
            </div>
        );
    }
}

class SvgStage extends React.Component {
    render() {
        const SvgOld = this.props.selStage > this.props.stage;
        const active = this.props.selStage === this.props.stage;
        const svg = <svg className="ufoLights d-none d-sm-block"><circle cx="25" cy="25" r="15" fill={ SvgOld ? "grey" : "white" } /></svg>;
        const text = <div className="text-white text-center h3">{this.props.text}</div>;
        return(
            <div className="col-10 col-sm-4 d-flex justify-content-center">
                { active ? text : svg }
            </div>
        );
    }
}

class SearchHeader extends React.Component {
    render() {
        var selStage = 0;
        switch(this.props.sel_type){
            case "supersection" :
                selStage = 1;
                break;
            case "section" :
                selStage = 2;
                break;
            case "theme" :
                selStage = 3;
                break;
        }
        return(
            <div className="container-fluid" id="search-header">
                <div className="container">
                    <div className="row justify-content-center align-items-center">
                        <SvgStage stage = {0} selStage = {selStage} text="Розділ" />
                        <SvgStage stage = {1} selStage = {selStage} text="Підрозділ" />
                        <SvgStage stage = {2} selStage = {selStage} text="Тема" />
                    </div>
                </div>
            </div>
        );
    }
}

function get_selector_data(selected_title, selected_type, materials){

    var selector = {
        "supersections" : {
            "selected" : "",
            "options" : []
        },
        "sections" : {
            "selected" : "",
            "options" : []
        },
        "themes" : {
            "selected" : "",
            "options" : [],
            "theme_info" : {}
        }
    };
    materials.map((material) => {
        if (!selector.supersections.options.includes(material.supersection)){
            selector.supersections.options.push(material.supersection);
        }
    });

    switch (selected_type){
        case "supersection" :
            selector.supersections.selected = selected_title;
            materials.map((material) => {
                if (material.supersection === selected_title){
                    selector.sections.options.push(material.title);
                }
            });
            break;
        case "section" :
            materials.map((material) => {
                if (material.title === selected_title){
                    selector.supersections.selected = material.supersection;
                    material.themes.map((theme) => {
                        selector.themes.options.push(theme.title);
                    });
                }
            });
            materials.map((material) => {
                if (material.supersection === selector.supersections.selected){
                    selector.sections.options.push(material.title);
                }
            });
            selector.sections.selected = selected_title;
            break;
        case "theme" :
            materials.map((material) => {
                material.themes.map((theme) => {
                    if (theme.title === selected_title){
                        selector.supersections.selected = material.supersection;
                        selector.sections.selected = material.title;
                        selector.themes.theme_info = theme;
                    }
                });
                selector.sections.options.push(material.title);
            });
            materials.map((material) => {
                if (material.title === selector.sections.selected){
                    material.themes.map((theme) => {
                        selector.themes.options.push(theme.title);
                    });
                }
            });
            selector.themes.selected = selected_title;
            break;
        default:
        }
    return selector;
}

class MaterialSearch extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selected_type : this.props.selected_type,
            selected_title : this.props.selected_title,
        };
        this.setSelected = this.setSelected.bind(this);
    }
    setSelected(sel_type, sel_title) {
        //Change the state
        this.setState({ selected_type : sel_type, selected_title : sel_title });
    }
    render() {
        const selector_data = get_selector_data(this.state.selected_title, this.state.selected_type, this.props.materials);
        
        return(
            <div className="container-fluid d-flex flex-column px-0" >
                <SearchHeader sel_type={this.state.selected_type} />
                <div className='container-fluid' id='material-selectors'>
                    <div className="container">
                        <div className="row h-100">
                            <Selector type="supersection" sel_title={selector_data.supersections.selected} options={selector_data.supersections.options} setSelected={this.setSelected} />                    
                            {selector_data.supersections.selected === "" ?
                            <div key="introduction" className="col-12 col-sm-6 mt-4 mx-auto d-sm-flex flex-column justify-content-center align-items-center text-white">
                                <h1 className="text-center border-bottom">Завдання по темам</h1>
                                <div className="pt-3"> Для кожної теми з фізики ми додали практичні та теоретичні завдання, які сортовані за складністю. Основою цих матеріалів можна вважати збірник задач О. Я. Савченко. 
                                    <br></br>
                                    <div className="text-center h5 pt-2">Виберіть <span className="d-none d-sm-inline">зліва</span><span className="d-sm-none">зверху</span> розділ фізики, який Вас цікавить!</div>
                                </div>
                            </div> : null
                            }
                            <Selector type="section" sel_title={selector_data.sections.selected} options={selector_data.sections.options} setSelected={this.setSelected} />
                            <Selector type="theme" sel_title={selector_data.themes.selected} options={selector_data.themes.options} setSelected={this.setSelected} />
                        </div>
                    </div>
                </div>
                { this.state.selected_type === "theme" ?
                    <MaterialInfo theme={selector_data.themes.theme_info} setSelected={this.setSelected} /> : null
                }
            </div>
        );
    }
}

fetch(`/materials_api`)
.then (response => response.json())
.then (materials => {
    const material = document.getElementById('material-search');
    const selected_type = material.dataset.selected_type;
    const selected_title = material.dataset.selected_title;
    ReactDOM.render(<MaterialSearch materials={materials} selected_type={selected_type} selected_title={selected_title} />, material);
});