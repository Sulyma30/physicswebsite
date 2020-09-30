class MaterialRow extends React.Component {
    render() {
      return (
        <tr style={this.props.style}>
            <td>{this.props.row.tasks}</td>
            <td></td>
            <td className="text-right pr-2">{this.props.row.literature.short_title} {this.props.row.literature.file ? <a href={this.props.row.literature.file}><i className="fas fa fa-download"></i></a> : null}</td>
        </tr>
      );
    }
  }

  class MaterialTable extends React.Component {
    render() {
      return (
        <table className="table table-striped mb-4">
          <tbody>
            {this.props.rows}
          </tbody>
        </table>
      );
    }
  }

  class AllTasks extends React.Component {
    render() {
      const all_rows = [];
      const all_style = {borderLeft: "4px solid lightgray"}
      this.props.all.forEach(row => {
        if (row.tasks){
            all_rows.push(
              <MaterialRow row={row} key={row.literature} style={all_style} />
            );
        }
      });
      return(
        <div className="tab-pane fade" id="all" role="tabpanel">
          <MaterialTable rows={all_rows} />
        </div>
      );
    }

  }

  class ChosenTasks extends React.Component {
    render() {
      const novice_rows = [];
      const novice_style={borderLeft: "4px solid lightgreen"};

      const advanced_rows = [];
      const advanced_style={borderLeft: "4px solid orange"};

      const expert_rows = [];
      const expert_style={borderLeft: "4px solid red"};

      this.props.chosen.novice.forEach((row) => {
          if (row.tasks){
              novice_rows.push(
                <MaterialRow row={row} key={row.literature} style={novice_style} />
              );
          } 
      });
      this.props.chosen.advanced.forEach((row) => {
        if (row.tasks){
            advanced_rows.push(
              <MaterialRow row={row} key={row.literature} style={advanced_style} />
            );
        }
      });
      this.props.chosen.expert.forEach((row) => {
        if (row.tasks){
            expert_rows.push(
              <MaterialRow row={row} key={row.literature} style={expert_style} />
            );
        }
      });

      return (
        <div className="tab-pane fade in show active" id="recommended" role="tabpanel">
          <MaterialTable rows={novice_rows} />
          <MaterialTable rows={advanced_rows} />
          <MaterialTable rows={expert_rows} />
        </div>
      );
    }
  }

//Here we should use type (problems or theory) and info about current theme (from material) and get information about neighbourhood themes and with url_for open the page (saving the type)
  class NextPrevious extends React.Component {
    render() {
      return (
        <div className="row justify-content-sm-between justify-content-center my-4">
          <div className="pl-3 col-sm-6 col-12 d-flex justify-content-center justify-content-sm-start">
        { this.props.previous ?
            <a href={"/materials/" + this.props.previous.id + "/" + this.props.task} className="btn btn-outline-bg"><i className="fas fa-lg fa-angle-left"></i> { this.props.previous.title } </a>
            : null }
          </div>
          <div className="pr-3 col-sm-6 col-12 d-flex justify-content-center justify-content-sm-end">
        { this.props.next ?
            <a href={"/materials/" + this.props.next.id + "/" + this.props.task} className="btn btn-outline-bg">{ this.props.next.title }<i className="fas fa-lg fa-angle-right"></i></a>
            : null }
          </div>
        </div>
      );
    }
  }

  class ContentHeaders extends React.Component {
    render() {
      return (
        <ul className="nav nav-pills material-pills mx-3">

          {
            this.props.task=="problems" ?
            <li className="nav-item px-0">
            <a className="nav-link active mx-0" id="recommended-tab" data-toggle="tab" href="#recommended" role="tab"
              aria-controls="recommended-tasks" aria-selected="true">Годні задачі</a></li> :
            <li className="nav-item px-0 pt-2">
            Сторінки
            </li>
          }

          {
            this.props.all.length != 0 ?
            <li className="nav-item px-0">
            <a className="nav-link mx-0" id="all-tab" data-toggle="tab" href="#all" role="tab" aria-controls="all-tasks"
              aria-selected="false">Всі</a>
          </li> : null
          }
          <li className="nav-item ml-auto pr-2 pt-2">
            Літ<span className="d-none d-sm-inline-block">ерату</span><span className="d-inline-block d-sm-none">-</span>ра
          </li>
        </ul>
      );
    }
  }


  class Content extends React.Component {
    render() {
      return (
        <div className="col-md-12 col-xl-8">
          <ContentHeaders all={this.props.tasks.all} task={this.props.task} />
          <div className="tab-content pt-1 px-3">
            <ChosenTasks chosen={this.props.tasks.chosen} />
            <AllTasks all={this.props.tasks.all} />
          </div>
          <NextPrevious next={this.props.connections.next} previous={this.props.connections.previous} task={this.props.task} />
        </div>
      );
    }
  } 
    //From backend I get type (problems or theory) and theme_id and with API I get material
    const material_content = document.getElementById('material-content')
    const task_type = material_content.dataset.task_type
    const theme_id = material_content.dataset.theme_id
    
    fetch(`/tasks/${theme_id}/${task_type}`)
    .then (response => response.json())
    .then (material => {
        console.log(material);
        ReactDOM.render(<Content tasks={material.tasks} task={task_type} connections={material.connections} />, material_content);
    });
