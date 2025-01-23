use crate::errors::ServiceError;
use crate::models::Course;
use crate::state::AppState;
use actix_web::{web, HttpResponse};
use super::db_access::*;

pub async fn health_check_handler(app_state: web::Data<AppState>) -> HttpResponse {
    let health_check_response = &app_state.health_check_response;
    let mut visit_count = app_state.visit_count.lock().unwrap(); // lock 防止多个线程更新
    let response = format!("{} {} times", health_check_response, visit_count);
    *visit_count += 1;
    HttpResponse::Ok().json(&response)
}

pub async fn new_course(
    new_course: web::Json<Course>,
    app_state: web::Data<AppState>,
) -> Result<HttpResponse,ServiceError> {
   post_new_course_db(&app_state.db, &new_course.into_inner()).await.map(|course|HttpResponse::Ok().json(course))
}

pub async fn get_courses_for_teacher(
    app_state: web::Data<AppState>,
    params: web::Path<usize>,
) -> Result<HttpResponse, ServiceError> {
    let teacher_id = i32::try_from(*params).expect("Failed to convert usize to i32");
    get_courses_for_teacher_db(&app_state.db, teacher_id)
        .await
        .map(|courses| HttpResponse::Ok().json(courses))
}

pub async fn get_course_detail(
    app_state: web::Data<AppState>,
    params: web::Path<(usize, usize)>,
) -> Result<HttpResponse, ServiceError> {
    let teacher_id = i32::try_from(params.0).unwrap();
    let course_id = i32::try_from(params.1).unwrap();
 get_course_details_db(&app_state.db, teacher_id, course_id).await.map(|course| HttpResponse::Ok().json(course))

}

#[cfg(test)]
mod tests {
    use super::*;
    use actix_web::http::StatusCode;
    use dotenv::dotenv;
    use sqlx::postgres::PgPoolOptions;
    use std::env;
    use std::sync::Mutex;

    #[actix_rt::test]
    async fn post_course_test() {
        dotenv().ok();

        let db_url = env::var("DATABASE_URL").expect("DATABASE_URL is not set in .env");
        let db_pool = PgPoolOptions::new().connect(&db_url).await.unwrap();

        let app_state: web::Data<AppState> = web::Data::new(AppState {
            health_check_response: "".to_string(),
            visit_count: Mutex::new(0),
            db: db_pool,
        });
        let course = web::Json(Course {
            teacher_id: 1,
            name: "Test course".into(),
            id: Some(24),
            time: None,
        });
        let resp = new_course(course, app_state).await.unwrap();
        assert_eq!(resp.status(), StatusCode::OK);
    }

    #[actix_rt::test]
    async fn get_all_course_success() {
        dotenv().ok();

        let db_url = env::var("DATABASE_URL").expect("DATABASE_URL is not set in .env");
        let db_pool = PgPoolOptions::new().connect(&db_url).await.unwrap();

        let app_state: web::Data<AppState> = web::Data::new(AppState {
            health_check_response: "".to_string(),
            visit_count: Mutex::new(0),
            db: db_pool,
        });
        let teacher_id: web::Path<usize> = web::Path::from(1);
        let resp = get_courses_for_teacher(app_state, teacher_id).await.unwrap() ;
        assert_eq!(resp.status(), StatusCode::OK);
    }

    #[actix_rt::test]
    async fn get_one_course_success() {
        dotenv().ok();

        let db_url = env::var("DATABASE_URL").expect("DATABASE_URL is not set in .env");
        let db_pool = PgPoolOptions::new().connect(&db_url).await.unwrap();

        let app_state: web::Data<AppState> = web::Data::new(AppState {
            health_check_response: "".to_string(),
            visit_count: Mutex::new(0),
            db: db_pool,
        });
        let params: web::Path<(usize, usize)> = web::Path::from((1, 1));
        let resp = get_course_detail(app_state, params).await.unwrap() ;
        assert_eq!(resp.status(), StatusCode::OK);
    }
}
