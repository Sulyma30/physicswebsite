class TourOptions extends React.Component {
    constructor(props) {
      super(props);
      this.handleChangeTour = this.handleChangeTour.bind(this);
    }
    handleChangeTour(tour, e) {
      this.props.handleChangeTour(tour);
    }
    render() {
      const options = [];
      this.props.tour_options.forEach(tour => {
        options.push(
          <li key={tour} className="nav-item">
            <a className={"nav-link "+ (this.props.tour === tour ? "active show " : "" )} onClick={(e) => this.handleChangeTour(tour, e)} data-toggle="tab" role="tab" aria-controls={tour} aria-selected={ this.props.tour == tour ? "true" : "false" }>
              {tour.substring(0, 4)}<span className="d-none d-md-inline-block">{tour.substring(4)}</span>
            </a>
          </li>
        );
      });
      return(
        <div className="mx-2">
          <ul className="nav justify-content-center" id="TourTab" role="tablist">
            {options}
          </ul>
        </div>
      )
    }
  }

  class GradeOptions extends React.Component {
    constructor(props) {
      super(props);
      this.handleChangeGrade = this.handleChangeGrade.bind(this);
    }
    handleChangeGrade(e) {
      this.props.handleChangeGrade(e);
    }
    componentDidUpdate() {
        $('.selectpicker').selectpicker('refresh');
    }
    componentDidMount() {
        $('.selectpicker').selectpicker('refresh');
    }
    render() {
      const options = [];
      this.props.grade_options.forEach(grade => {
        options.push(
          // Check whether it is 8-11 grades
          grade != 0 ?
          <option value={grade} key={grade} >{grade} клас</option> :
          <option value={grade} key={grade} >Всі класи</option>
        );
      });
      return(
        <select className="selectpicker" data-style="btn-bg olymp-files-select z-depth-0 px-1" data-width="130px" onChange={(e) => this.handleChangeGrade(e)} >
        {options}
        </select>
      )
    }
  }

  class YearOptions extends React.Component {
    constructor(props) {
          super(props);
          this.handleChangeEvent = this.handleChangeEvent.bind(this);
      }
      handleChangeEvent(e) {
          this.props.handleChangeEvent(e);
      }
      componentDidUpdate() {
        $('.selectpicker').selectpicker('refresh');
      }
      componentDidMount() {
        $('.selectpicker').selectpicker('refresh');
      }
     render() {
       const options = [];
       var i = 0;
        this.props.events.forEach(event => { 
          const subtext = this.props.type == 'national' ? event.location : "";
          options.push(
          <option value={i} key={event.year} data-subtext={subtext}>{event.year} рік</option>
          );
          i++;
        })
       return(
        <select className="selectpicker" data-style="btn-bg olymp-files-select z-depth-0 pl-2" data-width="140px" data-show-subtext="false" data-live-search="true" data-size="5" value={this.props.year} onChange={(e) => this.handleChangeEvent(e)}>
         {options}
         </select>
       );
     }
  }

  class DownloadButton extends React.Component {
    render() {
      var active_text = "Умови";
      var disabled_text = "Умов немає";
      if (this.props.solutions === true){
        active_text = "Розв'язки";
        disabled_text = "Розв'язків немає";
      }
      const btn_disabled = <button className="btn-md btn-white waves-effect px-1 py-4 olymp-files-btn z-depth-1 disabled">{disabled_text}</button>
      const btn_active = <a href={this.props.link} target="_blank" className="btn-lg btn-white waves-effect px-2 py-4 px-sm-3 olymp-files-btn z-depth-1">{active_text}<i className="fas fa fa-file-download"></i></a>
      return(
        <div className="d-flex justify-content-center px-1 col my-1">
          {this.props.link === "" ? btn_disabled : btn_active}
        </div>
      );
    }
  }

  class OlympSelector extends React.Component {
      constructor(props){
          super(props);
          this.state = {
              event : this.props.events[0],
              tour : this.props.events[0].files[0].tour,
              grade : this.props.events[0].files[0].grade
          };
          this.handleChangeEvent = this.handleChangeEvent.bind(this);
          this.handleChangeTour = this.handleChangeTour.bind(this);
          this.handleChangeGrade = this.handleChangeGrade.bind(this);
      }
      handleChangeEvent(event) {
          this.setState({ event : this.props.events[event.target.value] });
      }
      handleChangeTour(tour) {
          this.setState({ tour : tour });
      }
      handleChangeGrade(event) {
        this.setState({ grade : parseInt(event.target.value) });
      }

      render() {
        // Get links for files if they exist
          const links = {
            'problems' : "",
            'solutions' : ""
          };
          this.state.event.files.map((file) => {
            if (file.tour === this.state.tour && file.grade === this.state.grade){
              links['problems'] = file.problems === null ? "" : file.problems;
              links['solutions'] = file.solutions === null ? "" : file.solutions;
            }
          })
          return(
                <div className="pt-4">
                  <TourOptions tour={this.state.tour} tour_options={this.props.tour_options} handleChangeTour={this.handleChangeTour} />
                  <div id="olymp-files-selectors" className="row row-cols-2 row-cols-md-4 mx-1 px-1 py-3 justify-content-center z-depth-5">
                    <div className="col py-2" id="year-options">
                          <YearOptions type={this.props.type} events={this.props.events} tour={this.state.tour} year={this.state.year} handleChangeEvent={this.handleChangeEvent} />
                    </div>
                    <div className="col border-left py-2">
                          <GradeOptions grade_options={this.props.grade_options} grade={this.state.grade} handleChangeGrade={this.handleChangeGrade} />
                    </div>
                    <DownloadButton solutions={false} link={links.problems} />
                    <DownloadButton solutions={true} link={links.solutions} />
                  </div>
                </div>
          );
      }
  }

  class OlympFiles extends React.Component {
      render() {
        const tours = [];
        const grades = [];
        this.props.events.map((event) => {
          event.files.map((file) => {
            if (!tours.includes(file.tour)) {
              tours.push(file.tour);
            }
            if (!grades.includes(file.grade)) {
              grades.push(file.grade);
            }
          });
        })
        grades.sort((a, b) => b - a);
          return(
              <div className="d-flex flex-column justify-content-center align-items-center">
                  <OlympSelector type={this.props.type} tour_options={tours} grade_options={grades} events={this.props.events} />
              </div>
          );
      }
  }
//Type of olympiad ('national', 'regional',...)
olymp_files = document.getElementById('olymp-files')
const olymp_type = olymp_files.dataset.olymp_type
const static_location = olymp_files.dataset.static_location


fetch(`/olympiads_api/${olymp_type}/${static_location}`)
  .then (response => response.json())
  .then (olymp_events => {
      ReactDOM.render(<OlympFiles events={olymp_events} type={olymp_type} />, olymp_files);
  });
  