import BackgroundSVG from "./backgroundSVG";

function PageTemplate() {
  return (
    <div className="h-screen w-screen flex items-center justify-center outer-page">
      <div className="main_window bg-transparent">
        <BackgroundSVG />
      </div>
    </div>
  );
}

export default PageTemplate;
