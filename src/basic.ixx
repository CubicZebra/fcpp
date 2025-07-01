// Generated via simple_header_parser
export module basic;
import <functional>;
import <optional>;
#include <concepts>
#include <type_traits>

/**
 * @brief 2-d points
 */
export struct Point {
    float x; /**< X axis */
    float y; /**< Y axis */
};

/**
 * @brief the color aaaa
 */
export enum class Color {
    Red, /**< Red */
    Green, /**< Green */
    Blue, /**< Blue */
    Yellow /**< Yellow */
};


/**
 * @brief the color aaaaeee
 */
export enum class Color1 {
    Red, /**< Red */
    Green, /**< Green */
    Blue, /**< Blue */
    Yellow /**< Yellow */
};

/**
 * @brief Concept to check if a callable object can be invoked with specific arguments and return type.
 *
 * This concept verifies whether a given callable object (function, lambda, functor, etc.)
 * can be invoked with the specified argument types and produces a result that is convertible
 * to the desired return type. It leverages `std::is_invocable_r_v` from the C++ type traits library.
 *
 * @tparam F The callable object type (e.g., function pointer, lambda, or functor).
 * @tparam R The expected return type of the callable object when invoked.
 * @tparam Args The argument types that the callable object accepts.
 *
 * Usage example:
 * @code
 * auto lambda = [](int x, int y) -> int { return x + y; };
 * static_assert(Callable<decltype(lambda), int, int, int>, "Lambda is not callable with the specified signature!");
 * @endcode
 */
export template<typename F, typename R, typename... Args>
concept Callable = std::is_invocable_r_v<F, R, Args...>;

/**
 * @brief A concept that is always satisfied for any type.
 *
 * This concept is trivially true for all types. It can be used as a placeholder
 * or default concept in situations where no specific constraints are required
 * on the type. Essentially, it allows any type to satisfy this concept.
 *
 * @tparam T The type being checked (no restrictions).
 *
 * Usage example:
 * @code
 * template<typename T>
 * requires Any<T>
 * void process() {
 *     // This function accepts any type since `Any` is always true.
 * }
 *
 * process<int>();    // Valid: int satisfies `Any`.
 * process<std::string>(); // Valid: std::string satisfies `Any`.
 * @endcode
 */
template<typename T>
concept Any = true;

template<typename T>
concept Int = std::is_integral_v<T>;

template<typename T>
concept Float = std::is_floating_point_v<T>;

template <typename T>
concept Numeric = Int<T> || Float<T>;

// template<typename T>
// concept Optional = std::is_same_v<T, std::optional<typename T::value_type>>;  // >= C++17


template<typename T>
concept Optional = requires(T t) {
    { t.has_value() } -> std::convertible_to<bool>; // 确保有 has_value() 成员函数
    typename T::value_type;                         // 确保有 value_type 类型别名
};



template <Any T, typename F, typename... Args>
T test_func(F f, Args... args) {
    return f(args...);
}