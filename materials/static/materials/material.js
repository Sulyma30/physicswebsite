class MaterialRow extends React.Component {
    render() {
      var tasks = [];
      var file = "";
      if (this.props.row.literature.pdf){
        file = this.props.row.literature.pdf;
      }
      else if (this.props.row.literature.djvu){
        file = this.props.row.literature.djvu;
      }
      
      tasks = this.props.row.tasks.join(';   ');

      return (
        <tr style={this.props.style}>
            <td>{tasks}</td>
            <td></td>
            <td className="text-right pr-2">{this.props.row.literature.short_title} {file !== "" ? <a href={file}><i className="fas fa fa-download"></i></a> : null}</td>
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


  class Tasks extends React.Component {
    render() {
      const novice_rows = [];
      const novice_style={borderLeft: "4px solid lightgreen"};

      const advanced_rows = [];
      const advanced_style={borderLeft: "4px solid orange"};

      const expert_rows = [];
      const expert_style={borderLeft: "4px solid red"};

      const all_rows = [];
      const all_style = {borderLeft: "4px solid lightgray"}

      const math_rows = [];
      const math_style = {borderLeft: "4px solid pink"}

      this.props.taskSets.forEach((row) => {
        switch(row.difficulty){
          case 0:
            novice_rows.push(
              <MaterialRow row={row}  key={row.id} style={novice_style} task_type={this.props.task_type} />
            );
            break;
          case 1:
            advanced_rows.push(
              <MaterialRow row={row} key={row.id} style={advanced_style} task_type={this.props.task_type} />
            );
            break;
          case 2:
            expert_rows.push(
              <MaterialRow row={row} key={row.id} style={expert_style} task_type={this.props.task_type} />
            );
            break;
          case 3:
            math_rows.push(
              <MaterialRow row={row} key={row.id} style={math_style} task_type={this.props.task_type} />
            );
            break;
          default:
            all_rows.push(
              <MaterialRow row={row} key={row.id} style={all_style} task_type={this.props.task_type} />
            );
        }
      });
      return (
        <div className="tab-content pt-1 px-3">
          <div className="tab-pane fade in show active" id="recommended" role="tabpanel">
            <MaterialTable rows={novice_rows} />
            <MaterialTable rows={advanced_rows} />
            <MaterialTable rows={expert_rows} />
          </div>
          <div className="tab-pane fade" id="all" role="tabpanel">
            <MaterialTable rows={all_rows} />
            { math_rows.length !== 0 ?
            <div className="mr-auto mb-1">Матан</div> : null }   
              <MaterialTable rows={math_rows} /> 
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
            this.props.task_type=="problems" ?

            <li className="nav-item px-0">
            <a className="nav-link active mx-0" id="recommended-tab" data-toggle="tab" href="#recommended" role="tab"
              aria-controls="recommended-tasks" aria-selected="true">Годні задачі</a></li>:
  
            <li className="nav-item px-0 pt-2">
            Сторінки
            </li>
          }
          {
            this.props.task_type=="problems" ?

            <li className="nav-item px-0">
            <a className="nav-link mx-0" id="all-tab" data-toggle="tab" href="#all" role="tab" aria-controls="all-tasks"
              aria-selected="false">Всі</a></li>: null
          }

          <li className="nav-item ml-auto pr-2 pt-2">
            Літ<span className="d-none d-sm-inline-block">ерату</span><span className="d-inline-block d-sm-none">-</span>ра
          </li>
        </ul>
      );
    }
  }

// Add later:
// <NextPrevious next={this.props.connections.next} previous={this.props.connections.previous} task={this.props.task} />
  class Content extends React.Component {
    render() {
      return (
        <div className="col-md-12 col-xl-8">
          <ContentHeaders task_type={this.props.task_type} />
          <Tasks taskSets={this.props.taskSets} task_type={this.props.task_type} />
        </div>
      );
    }
  } 
    //From backend I get type (problems or theory) and theme_id and with API I get material
    const material_content = document.getElementById('material-content')
    const task_type = material_content.dataset.task_type
    const theme_id = material_content.dataset.theme_id
    
    fetch(`/materials_api/${theme_id}/${task_type}`)
    .then (response => response.json())
    .then (material => {
        ReactDOM.render(<Content taskSets={material} task_type={task_type} connections={material.connections} />, material_content);
    });
