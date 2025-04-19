#ifndef PLANE_H
#define PLANE_H

#include "DataType.h"
#include "Point.h"
#include "Line.h"
#include <vector>
#include <utility>
#include <stdexcept>
#include <iostream>
#include <set>
#include <cmath>


// Forward declarations
template <typename T>
class Plane;

template <typename T>
class Polygon;

// Plane class template
template <typename T = NType>
class Plane {
private:
    Point3D <T>  point_;    // A point on the plane
    Vector3D<T> normal_;    // A normal vector to the plane

public:
    // Constructors
    Plane() : point_(), 
              normal_(Vector3D<T>(static_cast<T>(0), static_cast<T>(0), static_cast<T>(1))) {}
    Plane(const Point3D<T>& point, const Vector3D<T>& normal) : point_(point), normal_(normal.normalized()) {}

    // Distance from a point to the plane
    T distance(const Point3D<T>& p) const {
        return normal_.dotProduct(p - point_);
    }

    // Intersection with a line
    Point3D<T> intersect(const Line<T>& l) const{
        auto denominator = normal_.dotProduct(l.getDirection());
        auto numerator = normal_.dotProduct(point_ - l.getPoint());
        if (denominator == static_cast<T>(0)) {
            if (numerator == static_cast<T>(0)) {
                throw std::runtime_error("Line on the plane");
            } else {
                throw std::runtime_error("Line is parallel to the plane");
            }
        }
        auto t = numerator / denominator;
        return l.getPoint() + l.getDirection() * t;
    }

    // Containment checks
    bool contains(const Point3D<T>& p) const {
        return distance(p) == static_cast<T>(0);
    }
    bool contains(const Line<T>& l) const {
        auto denominator = normal_.dotProduct(l.getDirection());
        auto numerator = normal_.dotProduct(point_ - l.getPoint());
        if (denominator == static_cast<T>(0) and numerator == static_cast<T>(0)) {
            return true;
        } else {
            return false;
        }
    }

    // Getters
    Point3D<T> getPoint() const { return point_; }
    Vector3D<T> getNormal() const { return normal_; }

    // Setters
    void setPoint(const Point3D<T>& point) { point_ = point; }
    void setNormal(const Vector3D<T>& normal) { normal_ = normal.normalized(); }

    // Operators
    bool operator==(const Plane& other) const;
    bool operator!=(const Plane& other) const { return !(*this == other); }

    // Output operator
    template <typename U>
    friend std::ostream& operator<<(std::ostream& os, const Plane<U>& plane);
};

// Polygon class template
template <typename T = NType>
class Polygon {
private:
    std::vector<Point3D<T>> vertices_;

public:
    // Constructors
    Polygon() : vertices_() {}
    Polygon(const std::vector<Point3D<T>>& vertices) : vertices_(vertices) {}

    // Getters
    std::vector<Point3D<T>> getVertices() const { return vertices_; }
    const Point3D<T>& getVertex(size_t index) const { return vertices_.at(index); }
    Plane<T>    getPlane   () const{
        // Min points: 3
        auto p = Plane<T>(vertices_[0], getNormal());
        return p;
    }
    // Get the plane    of the polygon
    Vector3D<T> getNormal  () const {
        Vector3D<T> n = Vector3D<T>(vertices_[1] - vertices_[0]).crossProduct(Vector3D<T>(vertices_[2] - vertices_[0]));
        // std::cout << n << std::endl;
        return n.normalized();
    }
    // Get the normal   of the polygon
    Point3D<T>  getCentroid() const {
        Point3D<T> c;
        for (auto v : vertices_) {
            c += v;
        }
        int num_v = vertices_.size();
        return c / static_cast<T>(num_v);
    }
    // Get the centroid of the polygon

    // Setters
    void setVertices(const std::vector<Point3D<T>>& vertices) { vertices_ = vertices; }

    // Check if a point is inside the polygon
    // Only works on poylgons CLOCKWISE
    bool contains(const Point3D<T>& p) const {
        Vector3D<T> n = getNormal();
        // check point in the plane
        auto dist_plane_to_point = n.dotProduct(p - vertices_[0]);
        if (dist_plane_to_point != static_cast<T>(0)) {
            return false;
        }
        // check point in the polygon, if any the sign is negatve, the point is not in the polygon
        int size = vertices_.size();

        for ( int i = 1; i < size; i++) {
            Vector3D<T> side = vertices_[i] - vertices_[i - 1];
            // std::cout << side;
            Vector3D<T> point_to_vertex = vertices_[i - 1] - p;
            // std::cout << point_to_vertex;
            Vector3D<T> tri_normal = side.crossProduct(point_to_vertex);
            // std::cout << tri_normal;

            // if the diretcion of the normal is different to the polygon normal, the point is outside
            if (n.dotProduct(tri_normal) < static_cast<T>(0)) {
                return false;
            }
        }
        // check last side
        Vector3D<T> last_side = vertices_[0] - vertices_[vertices_.size() - 1];
        Vector3D<T> last_point_to_vertex = vertices_[vertices_.size() - 1] - p;
        Vector3D<T> tri_normal = last_side.crossProduct(last_point_to_vertex);

        if (n.dotProduct(tri_normal) < static_cast<T>(0)) {
            return false;
        }
        return true;
    }

    // Get the relation of the polygon with a plane
    RelationType relationWithPlane(const Plane<T>& plane) const {
        std::vector<T> distances;
        for (auto vertex : vertices_) {
            T distance = plane.distance(vertex);
            distances.push_back(distance);
        }
        bool front = true;
        bool back = true;
        for (auto d : distances) {
            if (d > static_cast<T>(0)) {
                back = false;
            } else if (d < static_cast<T>(0)) {
                front = false;
            }
        }
        if (front and back) {
            return RelationType::COINCIDENT;
        } else if (front) {
            return RelationType::IN_FRONT;
        } else if (back) {
            return RelationType::BEHIND;
        }  else{
            return RelationType::SPLIT;
        }
    }

    // Split the polygon by a plane
    std::pair<Polygon<T>, Polygon<T>> split(const Plane<T>& plane) const {
        std::vector<Point3D<T>> fp;
        std::vector<Point3D<T>> bp;
        int size = vertices_.size();
        for (int i = 0; i < size -1; i++) {
            auto distance0 = plane.distance(vertices_[i]);
            auto distance1 = plane.distance(vertices_[i+1]);
            // std::cout << distance0 << " " << distance1 << std::endl;
            // curr vertex
            if (distance0 > static_cast<T>(0)) {
                fp.push_back(vertices_[i]);
            } else if (distance0 < static_cast<T>(0)) {
                bp.push_back(vertices_[i]);
            } else { // distance0 == 0
                fp.push_back(vertices_[i]);
                bp.push_back(vertices_[i]);
            }
            // polygon intersection
            if (((distance0 < static_cast<T>(0) and distance1 > static_cast<T>(0)) or (distance0 > static_cast<T>(0) and distance1 < static_cast<T>(0))) ) {
                auto intersection_point = plane.intersect(Line<T>(vertices_[i], vertices_[i+1]));
                fp.push_back(intersection_point);
                bp.push_back(intersection_point);
            }

        }
        // last vertex
        auto last_idx = vertices_.size() - 1;
        auto distance0 = plane.distance(vertices_[last_idx]);
        auto distance1 = plane.distance(vertices_[0]);
        // curr vertex
        if (distance0 > static_cast<T>(0)) {
            fp.push_back(vertices_[last_idx]);
        } else if (distance0 < static_cast<T>(0)) {
            bp.push_back(vertices_[last_idx]);
        } else { // distance0 == 0
            fp.push_back(vertices_[last_idx]);
            bp.push_back(vertices_[last_idx]);
        }
        // polygon intersection
        if (((distance0 < static_cast<T>(0) and distance1 > static_cast<T>(0)) or (distance0 > static_cast<T>(0) and distance1 < static_cast<T>(0))) ) {
            auto intersection_point = plane.intersect(Line<T>(vertices_[last_idx], vertices_[0]));
            fp.push_back(intersection_point);
            bp.push_back(intersection_point);
        }
        auto backP = Polygon<T>(bp);
        auto frontP = Polygon<T>(fp);
        // check area
        // std:: cout << "--------------" << std::endl;
        // std:: cout  << backP.area().getValue() << std::endl;
        // std:: cout  << frontP.area().getValue() << std::endl;
        // std:: cout << this->area().getValue() << std::endl;
        return {Polygon<T>(bp), Polygon<T>(fp) };

    }

    // Compute the area of the polygon
    T area() const{
        T res = static_cast<T>(0);
        // squares are
        int size = vertices_.size();
        for (int i = 0; i < size - 1; i++) {
            res = res + (vertices_[i] - getCentroid()).cross((vertices_[i+1] - getCentroid())).magnitude();
        }
        // last edge
        res += (vertices_[vertices_.size() - 1] -  getCentroid()).cross((vertices_[0] - getCentroid())).magnitude();
        // triangles area
        res = res / static_cast<T>(2);
        return res;
    }

    // Operators
    bool operator==(const Polygon& other) const;
    bool operator!=(const Polygon& other) const { return !(*this == other); }

    // Output operator
    template <typename U>
    friend std::ostream& operator<<(std::ostream& os, const Polygon<U>& polygon);
};


// Equality operators
template <typename T>
bool Plane<T>::operator==(const Plane<T>& other) const {
    bool normalsEqual = (normal_ == other.normal_) || (normal_ == -other.normal_);
    return normalsEqual && contains(other.point_);
}

// Output operator for Plane
template <typename T>
std::ostream& operator<<(std::ostream& os, const Plane<T>& plane) {
    os << "Point: " << plane.point_ << ", Normal: " << plane.normal_;
    return os;
}

// Equality operators
template <typename T>
bool Polygon<T>::operator==(const Polygon<T>& other) const {
    return vertices_ == other.vertices_;
}

// Output operator for Polygon
template <typename T>
std::ostream& operator<<(std::ostream& os, const Polygon<T>& polygon) {
    os << "Vertices: ";
    for (const auto& vertex : polygon.vertices_) {
        os << vertex << " ";
    }
    return os;
}

#endif // PLANE_H